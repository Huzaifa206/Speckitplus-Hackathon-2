"""
AI Agent for Task Management using Google Gemini
Handles natural language processing and tool execution
"""
import json
import logging
import html
import re
from typing import Dict, Any, List, Optional
from sqlmodel import Session, select
from core.gemini_client import get_gemini_client, get_gemini_model
from models.conversation import Conversation, ConversationCreate
from models.message import Message, MessageCreate, MessageRole
from core.database import get_db_session
from mcp_tools import add_task, list_tasks, complete_task, delete_task
import asyncio


def sanitize_input(input_text: str) -> str:
    """
    Sanitize user input to prevent injection attacks
    """
    # Remove potentially dangerous characters/sequences
    sanitized = html.escape(input_text)

    # Remove any potential SQL injection patterns
    sql_patterns = [
        r"(?i)(union\s+select)",
        r"(?i)(drop\s+table)",
        r"(?i)(delete\s+from)",
        r"(?i)(insert\s+into)",
        r"(?i)(update\s+\w+\s+set)",
        r"(?i)(exec\s*\()",
        r"(?i)(script\s*[:\s])",
    ]

    for pattern in sql_patterns:
        sanitized = re.sub(pattern, "", sanitized)

    # Limit length to prevent abuse
    MAX_INPUT_LENGTH = 1000
    if len(sanitized) > MAX_INPUT_LENGTH:
        sanitized = sanitized[:MAX_INPUT_LENGTH]

    return sanitized.strip()


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskManagementAgent:
    """Main agent class for handling task management conversations"""

    def __init__(self):
        self.client = get_gemini_client()
        self.model = get_gemini_model()

        # Define available tools for the agent
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string", "description": "The title of the task"},
                            "description": {"type": "string", "description": "Optional description of the task"},
                            "priority": {"type": "string", "description": "Priority level: high, medium, or low", "default": "medium"},
                            "due_date": {"type": "string", "description": "Due date in ISO format (YYYY-MM-DD)"},
                            "tags": {"type": "array", "items": {"type": "string"}, "description": "Optional tags for the task"}
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Retrieve user's tasks with optional filtering",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string", "description": "Filter by status: all, completed, or pending", "default": "all"},
                            "priority": {"type": "string", "description": "Filter by priority: all, high, medium, or low", "default": "all"},
                            "search": {"type": "string", "description": "Optional search term to filter tasks by title or description"}
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "The ID of the task to mark as completed"}
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Remove a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {"type": "integer", "description": "The ID of the task to delete"}
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]

    def process_message(self, user_input: str, user_id: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Process user input and return AI response with potential tool execution
        """
        try:
            # Sanitize user input
            sanitized_input = sanitize_input(user_input)

            # Load conversation history or create new one
            if conversation_id:
                conversation_uuid = conversation_id
                messages = self.load_conversation_history(conversation_uuid)
            else:
                # Create a new conversation
                conversation_uuid = self.create_new_conversation(user_id)
                messages = []

            # Add user message to the conversation
            user_message = {
                "role": "user",
                "content": sanitized_input
            }

            # Prepare messages for the model
            formatted_messages = [
                {
                    "role": "system",
                    "content": "You are a helpful task management assistant. Help users manage their tasks using natural language. "
                              "You can add, list, complete, and delete tasks. Always use the appropriate tools when needed. "
                              "Be concise and helpful in your responses."
                }
            ]

            # Add conversation history
            formatted_messages.extend(messages)
            # Add the current user message
            formatted_messages.append(user_message)

            # Call the Gemini model with tools
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=formatted_messages,
                    tools=self.tools,
                    tool_choice="auto"
                )
            except Exception as gemini_error:
                error_str = str(gemini_error)
                logger.error(f"Gemini API error: {error_str}")

                # Check if it's a rate limit error
                if "quota" in error_str.lower() or "rate" in error_str.lower() or "429" in error_str:
                    # Return a specific response for rate limit issues
                    return {
                        "conversation_id": conversation_uuid,
                        "response": "I've reached my API usage limit. Please wait before sending more requests, or check your Google Cloud quota settings.",
                        "tool_calls": [],
                        "timestamp": self.get_current_timestamp(),
                        "error": "Rate limit exceeded"
                    }
                else:
                    # Graceful degradation - return a helpful message to the user
                    return {
                        "conversation_id": conversation_uuid,
                        "response": "I'm currently unable to process your request due to an API issue. Please try again later.",
                        "tool_calls": [],
                        "timestamp": self.get_current_timestamp(),
                        "error": error_str
                    }

            # Process the response
            ai_response = response.choices[0]
            response_content = ""
            tool_calls = []

            if ai_response.finish_reason == "tool_calls":
                # Process tool calls
                for tool_call in ai_response.message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    # Execute the tool
                    result = self.execute_tool(function_name, function_args, user_id)

                    # Store the tool call for the response
                    tool_calls.append({
                        "tool_name": function_name,
                        "parameters": function_args,
                        "result": result
                    })

                # Get the final response after tool execution
                # For simplicity, we'll generate a follow-up message after tool execution
                follow_up_messages = formatted_messages.copy()
                # Add the tool call and result
                follow_up_messages.append({
                    "role": "assistant",
                    "content": ai_response.message.content or "",
                    "tool_calls": [tc for tc in tool_calls]
                })

                # Get final response from AI after tools were executed
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=follow_up_messages
                )

                response_content = final_response.choices[0].message.content

            else:
                # No tool calls, just return the AI response
                response_content = ai_response.message.content or ""

            # Save the conversation
            self.save_message(conversation_uuid, user_input, "user", user_id)
            self.save_message(conversation_uuid, response_content, "assistant", user_id, tool_calls)

            return {
                "conversation_id": conversation_uuid,
                "response": response_content,
                "tool_calls": tool_calls,
                "timestamp": self.get_current_timestamp()
            }

        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return {
                "conversation_id": conversation_id,
                "response": "Sorry, I encountered an error processing your request.",
                "tool_calls": [],
                "timestamp": self.get_current_timestamp(),
                "error": str(e)
            }

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        """Execute a tool with the given arguments"""
        try:
            if tool_name == "add_task":
                return add_task(user_id=user_id, **arguments)
            elif tool_name == "list_tasks":
                return list_tasks(user_id=user_id, **arguments)
            elif tool_name == "complete_task":
                return complete_task(user_id=user_id, **arguments)
            elif tool_name == "delete_task":
                return delete_task(user_id=user_id, **arguments)
            else:
                return {"success": False, "message": f"Unknown tool: {tool_name}"}
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return {"success": False, "message": f"Error executing tool: {str(e)}"}

    def load_conversation_history(self, conversation_uuid: str) -> List[Dict[str, str]]:
        """Load conversation history from the database"""
        try:
            with get_db_session() as session:
                # Get conversation by UUID
                from sqlalchemy import func
                conversation_stmt = select(Conversation).where(Conversation.uuid == conversation_uuid)
                conversation = session.exec(conversation_stmt).first()

                if not conversation:
                    return []

                # Get messages for this conversation
                message_stmt = select(Message).where(Message.conversation_id == conversation.id).order_by(Message.created_at)
                messages = session.exec(message_stmt).all()

                # Format messages for the AI
                formatted_messages = []
                for msg in messages:
                    formatted_msg = {
                        "role": msg.role.value,
                        "content": msg.content
                    }
                    if msg.tool_calls:
                        formatted_msg["tool_calls"] = json.loads(msg.tool_calls)
                    formatted_messages.append(formatted_msg)

                return formatted_messages
        except Exception as e:
            logger.error(f"Error loading conversation history: {str(e)}")
            return []

    def save_message(self, conversation_uuid: str, content: str, role: str, user_id: str, tool_calls: Optional[List[Dict]] = None):
        """Save a message to the conversation"""
        try:
            with get_db_session() as session:
                # Get conversation by UUID
                conversation_stmt = select(Conversation).where(Conversation.uuid == conversation_uuid)
                conversation = session.exec(conversation_stmt).first()

                if not conversation:
                    # Create a new conversation if it doesn't exist
                    conversation = Conversation(
                        title=content[:50] + "..." if len(content) > 50 else content,
                        user_id=user_id,
                        is_active=True
                    )
                    session.add(conversation)
                    session.commit()
                    session.refresh(conversation)

                # Create the message
                message_data = Message(
                    role=MessageRole(role),
                    content=content,
                    conversation_id=conversation.id
                )

                if tool_calls:
                    message_data.tool_calls = json.dumps(tool_calls)

                session.add(message_data)
                session.commit()
        except Exception as e:
            logger.error(f"Error saving message: {str(e)}")

    def create_new_conversation(self, user_id: str) -> str:
        """Create a new conversation and return its UUID"""
        try:
            with get_db_session() as session:
                # Create a new conversation
                conversation = Conversation(
                    title="New Conversation",
                    user_id=user_id,
                    is_active=True
                )
                session.add(conversation)
                session.commit()
                session.refresh(conversation)

                return conversation.uuid
        except Exception as e:
            logger.error(f"Error creating new conversation: {str(e)}")
            # Return a default conversation UUID
            import uuid
            return str(uuid.uuid4())

    def get_current_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime
        return datetime.utcnow().isoformat() + "Z"


# Global agent instance
agent = TaskManagementAgent()


def process_user_message(user_input: str, user_id: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
    """Public function to process user messages"""
    return agent.process_message(user_input, user_id, conversation_id)