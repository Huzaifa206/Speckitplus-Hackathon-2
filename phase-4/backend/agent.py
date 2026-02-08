"""
AI Agent for Task Management using Google Gemini
Handles natural language processing and tool execution
"""
import json
import logging
import html
import re
import time
import random
from typing import Dict, Any, List, Optional
from sqlmodel import Session, select
from core.gemini_client import get_gemini_client, get_gemini_model
from models.conversation import Conversation, ConversationCreate
from models.message import Message, MessageCreate, MessageRole
from core.database import get_db_session
from mcp_tools import add_task, list_tasks, complete_task, delete_task
import asyncio
from openai import RateLimitError

# Import Pydantic models for structured output
from structured_output_models import TaskCommand


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
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum time between requests in seconds

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

            # Prepare system instructions
            system_instructions = ("You are a task management assistant. Help users manage their tasks.\n\n"
                                  "When users want to delete or complete a task:\n"
                                  "- If they just say 'delete' without specifying which task, ask them to specify the task name\n"
                                  "- To delete: Say 'Which task would you like to delete? Please provide the task name.'\n"
                                  "- To complete: Say 'Which task would you like to complete? Please provide the task name.'\n"
                                  "- When they provide the name, search the task list and perform the operation\n\n"
                                  "To add tasks, use the add_task function with title, description, priority, due_date, and tags.\n"
                                  "To list tasks, use the list_tasks function.\n\n")

            # Prepare messages - include system instructions with first message if no history
            formatted_messages = []

            if not messages:
                # First message in conversation - prepend system instructions
                formatted_messages.append({
                    "role": "user",
                    "content": system_instructions + "User: " + sanitized_input
                })
            else:
                # Has history - add conversation history then current message
                formatted_messages.extend(messages)
                formatted_messages.append(user_message)

            # Implement minimal delay between requests to respect rate limits
            current_time = time.time()
            time_since_last_request = current_time - self.last_request_time
            if time_since_last_request < self.min_request_interval:
                time.sleep(self.min_request_interval - time_since_last_request)

            # Call the Gemini model with function calling capability
            try:
                print(f"DEBUG: Calling Gemini API with {len(formatted_messages)} messages")

                # Prepare tools for function calling
                from structured_output_models import FUNCTION_DEFINITIONS

                # Try calling with tools first (function calling)
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=formatted_messages,
                        tools=[{
                            "type": "function",
                            "function": tool_def
                        } for tool_def in FUNCTION_DEFINITIONS],
                        tool_choice="auto"  # Allow model to choose when to use functions
                    )

                    # Update last request time after successful call
                    self.last_request_time = time.time()

                    # Check if the model chose to call a function
                    if response.choices[0].message.tool_calls:
                        # Process the tool calls
                        tool_calls = []
                        response_content = ""

                        for tool_call in response.choices[0].message.tool_calls:
                            function_name = tool_call.function.name
                            function_args = json.loads(tool_call.function.arguments)

                            # Execute the tool
                            result = self.execute_tool(function_name, function_args, user_id)

                            # Add to tool calls list
                            tool_calls.append({
                                "tool_name": function_name,
                                "parameters": function_args,
                                "result": result
                            })

                            # Create a user-friendly response
                            if result.get("success"):
                                if function_name == "add_task":
                                    response_content = result.get("message", f"Task '{function_args.get('title', 'Untitled')}' added successfully!")
                                elif function_name == "list_tasks":
                                    tasks = result.get("tasks", [])
                                    if tasks:
                                        # Store task ID mapping for this conversation (index -> database ID)
                                        # This allows users to reference tasks by simple numbers like 1, 2, 3
                                        if not hasattr(self, 'task_id_map'):
                                            self.task_id_map = {}
                                        if conversation_uuid not in self.task_id_map:
                                            self.task_id_map[conversation_uuid] = {}

                                        task_lines = []
                                        for index, task in enumerate(tasks, start=1):
                                            # Map simple index to actual database ID
                                            self.task_id_map[conversation_uuid][index] = task['id']

                                            status = "✓ Completed" if task.get('completed', False) else "○ Pending"
                                            task_lines.append(f"{index}. {task['title']} (Priority: {task['priority']}, {status})")
                                        response_content = "Here are your tasks:\n" + "\n".join(task_lines) + "\n\nYou can use the numbers (1, 2, 3...) to delete or complete tasks."
                                    else:
                                        response_content = "You don't have any tasks matching those criteria."
                                elif function_name == "complete_task":
                                    # If the function was called with a display index, map it to database ID
                                    task_id_param = function_args.get('task_id', 'unknown')

                                    # Check if this is a display index that needs mapping
                                    actual_task_id = task_id_param
                                    if isinstance(task_id_param, int) and hasattr(self, 'task_id_map') and conversation_uuid in self.task_id_map:
                                        actual_task_id = self.task_id_map[conversation_uuid].get(task_id_param, task_id_param)

                                    # Execute with the actual database ID
                                    result = self.execute_tool("complete_task", {"task_id": actual_task_id}, user_id)
                                    response_content = result.get("message", f"Task {task_id_param} marked as complete!")
                                elif function_name == "delete_task":
                                    # If the function was called with a display index, map it to database ID
                                    task_id_param = function_args.get('task_id', 'unknown')

                                    # Check if this is a display index that needs mapping
                                    actual_task_id = task_id_param
                                    if isinstance(task_id_param, int) and hasattr(self, 'task_id_map') and conversation_uuid in self.task_id_map:
                                        actual_task_id = self.task_id_map[conversation_uuid].get(task_id_param, task_id_param)

                                    # Execute with the actual database ID
                                    result = self.execute_tool("delete_task", {"task_id": actual_task_id}, user_id)
                                    response_content = result.get("message", f"Task {task_id_param} deleted successfully!")
                                else:
                                    response_content = result.get("message", f"Operation completed successfully.")
                            else:
                                response_content = result.get("message", f"Failed to execute {function_name}: {result.get('error', 'Unknown error')}")
                    else:
                        # No tool calls were made, use the regular content
                        response_content = response.choices[0].message.content or ""
                        tool_calls = []

                except Exception as tool_error:
                    print(f"DEBUG: Function calling failed, falling back to structured prompting: {str(tool_error)}")

                    # Fallback to the original approach
                    print(f"DEBUG: System message length: {len(formatted_messages[0]['content']) if formatted_messages else 0}")

                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=formatted_messages
                    )

                    # Update last request time after successful call
                    self.last_request_time = time.time()

                    # Process the response
                    ai_response = response.choices[0]
                    response_content = ai_response.message.content or ""

                    print(f"DEBUG: Gemini response: {response_content[:200]}...")

                    tool_calls = []

                # Check if the response contains structured commands (fallback parsing)
                import re
                task_add_match = re.search(r'TASK_ADD:\s*(.+)', response_content, re.IGNORECASE)
                if task_add_match:
                    # Parse task details
                    task_details_str = task_add_match.group(1).strip()

                    # Extract individual fields
                    title_match = re.search(r'title:\s*([^\n,\[]+)', task_details_str, re.IGNORECASE)
                    desc_match = re.search(r'description:\s*([^\n,\[]+)', task_details_str, re.IGNORECASE)
                    priority_match = re.search(r'priority:\s*(high|medium|low)', task_details_str, re.IGNORECASE)
                    due_date_match = re.search(r'due_date:\s*((\d{4}-\d{2}-\d{2})|(\d{2}-\d{2}-\d{4}))', task_details_str, re.IGNORECASE)
                    tags_match = re.search(r'tags:\s*\[(.*?)\]', task_details_str, re.IGNORECASE)  # Look for tags in brackets

                    if title_match:
                        title = title_match.group(1).strip().strip('"\'')

                        # Build arguments dictionary
                        task_args = {"title": title}

                        if desc_match:
                            task_args["description"] = desc_match.group(1).strip().strip('"\'')

                        if priority_match:
                            task_args["priority"] = priority_match.group(1).strip()

                        if due_date_match:
                            task_args["due_date"] = due_date_match.group(1).strip()

                        if tags_match:
                            # Parse tags from bracket notation
                            tags_str = tags_match.group(1)
                            tags = [tag.strip().strip('"\'') for tag in tags_str.split(',') if tag.strip()]
                            # Convert to JSON string for storage
                            task_args["tags"] = json.dumps(tags) if tags else "[]"

                        # Execute the tool manually
                        result = self.execute_tool("add_task", task_args, user_id)
                        tool_calls.append({
                            "tool_name": "add_task",
                            "parameters": task_args,
                            "result": result
                        })

                        # Update response to be more user-friendly
                        if result.get("success"):
                            # If there's an active task mapping, add the new task to it
                            if hasattr(self, 'task_id_map') and conversation_uuid in self.task_id_map:
                                # Find the next available display index
                                existing_indices = set(self.task_id_map[conversation_uuid].keys())
                                next_index = 1
                                while next_index in existing_indices:
                                    next_index += 1

                                # Add the new task to the mapping
                                task_id = result.get("task", {}).get("id", result.get("task_id"))
                                if task_id:
                                    self.task_id_map[conversation_uuid][next_index] = task_id
                                    print(f"DEBUG: Added new task to mapping: display {next_index} -> database {task_id}")

                            response_content = result.get("message", f"Task '{title}' added successfully!")
                        else:
                            response_content = result.get("message", f"Failed to add task: {result.get('error', 'Unknown error')}")

                # Look for task list command
                task_list_match = re.search(r'TASK_LIST:\s*(.+)', response_content, re.IGNORECASE)
                if task_list_match:
                    # Parse list parameters
                    list_params_str = task_list_match.group(1).strip()

                    # Extract individual fields
                    status_match = re.search(r'status:\s*(all|completed|pending)', list_params_str, re.IGNORECASE)
                    priority_match = re.search(r'priority:\s*(all|high|medium|low)', list_params_str, re.IGNORECASE)
                    search_match = re.search(r'search:\s*([^\n\[]+)', list_params_str, re.IGNORECASE)

                    list_args = {}
                    if status_match:
                        list_args["status"] = status_match.group(1).strip()
                    if priority_match:
                        list_args["priority"] = priority_match.group(1).strip()
                    if search_match:
                        list_args["search"] = search_match.group(1).strip().strip('"\'')

                    # Execute the tool manually
                    result = self.execute_tool("list_tasks", list_args, user_id)
                    tool_calls.append({
                        "tool_name": "list_tasks",
                        "parameters": list_args,
                        "result": result
                    })

                    # Format the response nicely
                    if result.get("success"):
                        tasks = result.get("tasks", [])
                        if tasks:
                            # Store task ID mapping for this conversation (index -> database ID)
                            # This allows users to reference tasks by simple numbers like 1, 2, 3
                            if not hasattr(self, 'task_id_map'):
                                self.task_id_map = {}
                            if conversation_uuid not in self.task_id_map:
                                self.task_id_map[conversation_uuid] = {}

                            task_lines = []
                            for index, task in enumerate(tasks, start=1):
                                # Map simple index to actual database ID
                                self.task_id_map[conversation_uuid][index] = task['id']

                                status = "✓ Completed" if task.get('completed', False) else "○ Pending"
                                task_lines.append(f"{index}. {task['title']} (Priority: {task['priority']}, {status})")
                            response_content = "Here are your tasks:\n" + "\n".join(task_lines) + "\n\nYou can use the numbers (1, 2, 3...) to delete or complete tasks."
                        else:
                            response_content = "You don't have any tasks matching those criteria."
                    else:
                        response_content = f"Failed to list tasks: {result.get('error', 'Unknown error')}"

                # Look for task complete command
                task_complete_match = re.search(r'TASK_COMPLETE:\s*task_id:\s*(\d+)', response_content, re.IGNORECASE)
                if task_complete_match:
                    display_index = int(task_complete_match.group(1))

                    # Convert display index to actual database ID
                    actual_task_id = None

                    if hasattr(self, 'task_id_map') and conversation_uuid in self.task_id_map:
                        print(f"DEBUG: Found mapping for conversation {conversation_uuid}, available indices: {list(self.task_id_map[conversation_uuid].keys())}")
                        actual_task_id = self.task_id_map[conversation_uuid].get(display_index)
                        if actual_task_id:
                            print(f"DEBUG: Using mapping - Converted {display_index} -> {actual_task_id}")
                        else:
                            print(f"DEBUG: No mapping found for index {display_index}, will fetch current task list")
                    else:
                        print(f"DEBUG: No mapping found, will fetch current task list")

                    # If we don't have a mapping or the mapping doesn't have this index, get current task list
                    if actual_task_id is None:
                        print(f"DEBUG: Fetching current task list to determine task ID for position {display_index}")
                        # Get the current list of tasks for this user (this will be in the same order as the UI)
                        list_result = self.execute_tool("list_tasks", {}, user_id)
                        print(f"DEBUG: list_tasks result success: {list_result.get('success')}, tasks count: {len(list_result.get('tasks', []))}")
                        if list_result.get("success"):
                            tasks = list_result.get("tasks", [])
                            print(f"DEBUG: Task IDs in list: {[t['id'] for t in tasks]}")
                            if display_index <= len(tasks) and display_index > 0:
                                actual_task_id = tasks[display_index - 1]["id"]  # -1 for 0-based indexing
                                print(f"DEBUG: Retrieved task ID {actual_task_id} for display position {display_index}")
                            else:
                                print(f"DEBUG: Display index {display_index} out of range (1-{len(tasks)})")

                    # Only execute if we have a valid task_id
                    if actual_task_id is not None:
                        args = {"task_id": actual_task_id}

                        # Execute the tool manually
                        result = self.execute_tool("complete_task", args, user_id)
                        tool_calls.append({
                            "tool_name": "complete_task",
                            "parameters": args,
                            "result": result
                        })

                        # Update response
                        if result.get("success"):
                            response_content = result.get("message", f"Task {display_index} marked as complete!")
                        else:
                            response_content = result.get("message", f"Failed to complete task {display_index}.")
                    else:
                        response_content = f"Task #{display_index} doesn't exist or could not be found."

                # Look for task delete command
                task_delete_match = re.search(r'TASK_DELETE:\s*task_id:\s*(\d+)', response_content, re.IGNORECASE)
                if task_delete_match:
                    print(f"DEBUG: TASK_DELETE command detected in response")
                    display_index = int(task_delete_match.group(1))
                    print(f"DEBUG: Display index from command: {display_index}")

                    # Convert display index to actual database ID
                    actual_task_id = None

                    print(f"DEBUG: Checking task_id_map - hasattr: {hasattr(self, 'task_id_map')}")
                    if hasattr(self, 'task_id_map'):
                        print(f"DEBUG: task_id_map exists, conversations: {list(self.task_id_map.keys())}")
                        print(f"DEBUG: Current conversation_uuid: {conversation_uuid}")

                    if hasattr(self, 'task_id_map') and conversation_uuid in self.task_id_map:
                        print(f"DEBUG: Found mapping for conversation {conversation_uuid}, available indices: {list(self.task_id_map[conversation_uuid].keys())}")
                        actual_task_id = self.task_id_map[conversation_uuid].get(display_index)
                        if actual_task_id:
                            print(f"DEBUG: Using mapping - Converted {display_index} -> {actual_task_id}")
                        else:
                            print(f"DEBUG: No mapping found for index {display_index}, will fetch current task list")
                    else:
                        print(f"DEBUG: No mapping found for this conversation, will fetch current task list")

                    # If we don't have a mapping or the mapping doesn't have this index, get current task list
                    if actual_task_id is None:
                        print(f"DEBUG: Fetching current task list to determine task ID for position {display_index}")
                        # Get the current list of tasks for this user (this will be in the same order as the UI)
                        list_result = self.execute_tool("list_tasks", {}, user_id)
                        print(f"DEBUG: list_tasks result success: {list_result.get('success')}, tasks count: {len(list_result.get('tasks', []))}")
                        if list_result.get("success"):
                            tasks = list_result.get("tasks", [])
                            print(f"DEBUG: Task IDs in list: {[t['id'] for t in tasks]}")
                            if display_index <= len(tasks) and display_index > 0:
                                actual_task_id = tasks[display_index - 1]["id"]  # -1 for 0-based indexing
                                print(f"DEBUG: Retrieved task ID {actual_task_id} for display position {display_index}")
                            else:
                                print(f"DEBUG: Display index {display_index} out of range (1-{len(tasks)})")

                    # Only execute if we have a valid task_id
                    if actual_task_id is not None:
                        args = {"task_id": actual_task_id}

                        # Execute the tool manually
                        result = self.execute_tool("delete_task", args, user_id)
                        tool_calls.append({
                            "tool_name": "delete_task",
                            "parameters": args,
                            "result": result
                        })

                        # Update response
                        if result.get("success"):
                            response_content = result.get("message", f"Task {display_index} deleted successfully!")
                        else:
                            response_content = result.get("message", f"Failed to delete task {display_index}.")
                    else:
                        response_content = f"Task #{display_index} doesn't exist or could not be found."

                # If no structured commands were found, try to parse natural language commands from original user input
                if not tool_calls and user_input:
                    print(f"DEBUG: No structured commands found, checking natural language for: {user_input}")
                    import re

                    # Check for delete command in user input
                    delete_patterns = [
                        r'delete\s+(\d+)',
                        r'delete.*?(\d+)',
                        r'remove.*?(\d+)',
                        r'task.*?(\d+).*?delete',
                        r'delete.*?task.*?(\d+)',
                        r'remove.*?task.*?(\d+)'
                    ]

                    for pattern in delete_patterns:
                        delete_match = re.search(pattern, user_input, re.IGNORECASE)
                        if delete_match:
                            print(f"DEBUG: Found delete pattern match: {delete_match.group(0)}")
                            display_index = int(delete_match.group(1))

                            # If there's no mapping, get the current task list to determine the mapping
                            actual_task_id = None

                            if hasattr(self, 'task_id_map') and conversation_uuid in self.task_id_map:
                                print(f"DEBUG: Found mapping for conversation {conversation_uuid}, available indices: {list(self.task_id_map[conversation_uuid].keys())}")
                                actual_task_id = self.task_id_map[conversation_uuid].get(display_index)
                                if actual_task_id:
                                    print(f"DEBUG: Using mapping - Converted {display_index} -> {actual_task_id}")
                                else:
                                    print(f"DEBUG: No mapping found for index {display_index}, will fetch current task list")
                            else:
                                print(f"DEBUG: No mapping found, will fetch current task list")

                            # If we don't have a mapping or the mapping doesn't have this index, get current task list
                            if actual_task_id is None:
                                print(f"DEBUG: Fetching current task list to determine task ID for position {display_index}")
                                # Get the current list of tasks for this user (this will be in the same order as the UI)
                                list_result = self.execute_tool("list_tasks", {}, user_id)
                                if list_result.get("success"):
                                    tasks = list_result.get("tasks", [])
                                    if display_index <= len(tasks) and display_index > 0:
                                        actual_task_id = tasks[display_index - 1]["id"]  # -1 for 0-based indexing
                                        print(f"DEBUG: Retrieved task ID {actual_task_id} for display position {display_index}")
                                    else:
                                        response_content = f"Task #{display_index} doesn't exist. You only have {len(tasks)} task(s)."
                                        tool_calls = []
                                        break
                                else:
                                    response_content = "Could not retrieve task list to determine which task to delete."
                                    tool_calls = []
                                    break

                            args = {"task_id": actual_task_id}
                            result = self.execute_tool("delete_task", args, user_id)

                            response_content = result.get("message", f"Task {display_index} {'deleted successfully!' if result.get('success') else 'could not be deleted.'}")

                            tool_calls = [{
                                "tool_name": "delete_task",
                                "parameters": args,
                                "result": result
                            }]
                            print(f"DEBUG: Delete operation executed, success: {result.get('success')}")
                            break  # Process only the first match

                    # If no number-based deletion was processed, try to match by task name/title
                    if not tool_calls:
                        # Look for patterns like "delete task with title [title]", "delete [title]", etc.
                        import re
                        title_patterns = [
                            r'delete\s+([a-zA-Z][a-zA-Z\s]+)$',  # delete taskname (simple word or phrase at end)
                            r'delete.*?["\']([^"\']+)["\']',  # delete "task name" or delete 'task name'
                            r'remove\s+([a-zA-Z][a-zA-Z\s]+)$',  # remove taskname
                            r'remove.*?["\']([^"\']+)["\']',  # remove "task name"
                            r'delete\s+task\s+([a-zA-Z][a-zA-Z\s]+)$',  # delete task taskname
                        ]

                        for pattern in title_patterns:
                            title_match = re.search(pattern, user_input, re.IGNORECASE)
                            if title_match:
                                task_title = title_match.group(1).strip()
                                print(f"DEBUG: Found task title to delete: {task_title}")

                                # Skip if the title is too short or looks like a command
                                if len(task_title) < 2 or task_title.lower() in ['task', 'it', 'this', 'that']:
                                    print(f"DEBUG: Skipping invalid title: {task_title}")
                                    continue

                                # Get the current list of tasks to find the matching title
                                list_result = self.execute_tool("list_tasks", {}, user_id)
                                if list_result.get("success"):
                                    tasks = list_result.get("tasks", [])

                                    # Find the task with the matching title (case-insensitive)
                                    matched_task = None
                                    for task in tasks:
                                        if task_title.lower() in task["title"].lower():
                                            matched_task = task
                                            break

                                    if matched_task:
                                        actual_task_id = matched_task["id"]
                                        args = {"task_id": actual_task_id}
                                        result = self.execute_tool("delete_task", args, user_id)

                                        response_content = result.get("message", f"Task '{task_title}' {'deleted successfully!' if result.get('success') else 'could not be deleted.'}")

                                        tool_calls = [{
                                            "tool_name": "delete_task",
                                            "parameters": args,
                                            "result": result
                                        }]
                                        print(f"DEBUG: Delete by title operation executed, success: {result.get('success')}")
                                        break
                                    else:
                                        response_content = f"No task found with title containing '{task_title}'. Available tasks: {[t['title'] for t in tasks]}"
                                        tool_calls = []
                                        break
                                else:
                                    print(f"DEBUG: list_tasks failed when trying to delete by title: {list_result}")
                                    response_content = f"Could not find task with title '{task_title}' to delete."
                                    tool_calls = []
                                    break

                    # Check for complete command in user input if no delete was processed
                    if not tool_calls:  # Only process if no delete was processed
                        print(f"DEBUG: Checking for complete commands in: {user_input}")
                        complete_patterns = [
                            r'complete\s+(\d+)',
                            r'complete.*?(\d+)',
                            r'finish.*?(\d+)',
                            r'mark.*?(\d+).*?done',
                            r'mark.*?(\d+).*?complete',
                            r'complete.*?task.*?(\d+)',
                            r'finish.*?task.*?(\d+)'
                        ]

                        for pattern in complete_patterns:
                            complete_match = re.search(pattern, user_input, re.IGNORECASE)
                            if complete_match:
                                print(f"DEBUG: Found complete pattern match: {complete_match.group(0)}")
                                display_index = int(complete_match.group(1))

                                # If there's no mapping, get the current task list to determine the mapping
                                actual_task_id = None

                                if hasattr(self, 'task_id_map') and conversation_uuid in self.task_id_map:
                                    print(f"DEBUG: Found mapping for conversation {conversation_uuid}, available indices: {list(self.task_id_map[conversation_uuid].keys())}")
                                    actual_task_id = self.task_id_map[conversation_uuid].get(display_index)
                                    if actual_task_id:
                                        print(f"DEBUG: Using mapping - Converted {display_index} -> {actual_task_id}")
                                    else:
                                        print(f"DEBUG: No mapping found for index {display_index}, will fetch current task list")
                                else:
                                    print(f"DEBUG: No mapping found, will fetch current task list")

                                # If we don't have a mapping or the mapping doesn't have this index, get current task list
                                if actual_task_id is None:
                                    print(f"DEBUG: Fetching current task list to determine task ID for position {display_index}")
                                    # Get the current list of tasks for this user (this will be in the same order as the UI)
                                    list_result = self.execute_tool("list_tasks", {}, user_id)
                                    if list_result.get("success"):
                                        tasks = list_result.get("tasks", [])
                                        if display_index <= len(tasks) and display_index > 0:
                                            actual_task_id = tasks[display_index - 1]["id"]  # -1 for 0-based indexing
                                            print(f"DEBUG: Retrieved task ID {actual_task_id} for display position {display_index}")
                                        else:
                                            response_content = f"Task #{display_index} doesn't exist. You only have {len(tasks)} task(s)."
                                            tool_calls = []
                                            break
                                    else:
                                        response_content = "Could not retrieve task list to determine which task to complete."
                                        tool_calls = []
                                        break

                                args = {"task_id": actual_task_id}
                                result = self.execute_tool("complete_task", args, user_id)

                                response_content = result.get("message", f"Task {display_index} {'marked as complete!' if result.get('success') else 'could not be completed.'}")

                                tool_calls = [{
                                    "tool_name": "complete_task",
                                    "parameters": args,
                                    "result": result
                                }]
                                print(f"DEBUG: Complete operation executed, success: {result.get('success')}")
                                break  # Process only the first match

                    # If no number-based completion was processed, try to match by task name/title
                    if not tool_calls:  # Only if no number-based completion was processed
                        # Look for patterns like "complete task with title [title]", "complete [title]", etc.
                        import re
                        complete_title_patterns = [
                            r'complete\s+([a-zA-Z][a-zA-Z\s]+)$',  # complete taskname (simple word or phrase at end)
                            r'complete.*?["\']([^"\']+)["\']',  # complete "task name" or complete 'task name'
                            r'finish\s+([a-zA-Z][a-zA-Z\s]+)$',   # finish taskname
                            r'finish.*?["\']([^"\']+)["\']',   # finish "task name"
                            r'complete\s+task\s+([a-zA-Z][a-zA-Z\s]+)$',  # complete task taskname
                            r'mark.*?["\']([^"\']+)["\'].*?done',  # mark "task" done
                            r'mark.*?["\']([^"\']+)["\'].*?complete',  # mark "task" complete
                        ]

                        for pattern in complete_title_patterns:
                            title_match = re.search(pattern, user_input, re.IGNORECASE)
                            if title_match:
                                task_title = title_match.group(1).strip()
                                print(f"DEBUG: Found task title to complete: {task_title}")

                                # Skip if the title is too short or looks like a command
                                if len(task_title) < 2 or task_title.lower() in ['task', 'it', 'this', 'that']:
                                    print(f"DEBUG: Skipping invalid title: {task_title}")
                                    continue

                                # Get the current list of tasks to find the matching title
                                list_result = self.execute_tool("list_tasks", {}, user_id)
                                if list_result.get("success"):
                                    tasks = list_result.get("tasks", [])

                                    # Find the task with the matching title (case-insensitive)
                                    matched_task = None
                                    for task in tasks:
                                        if task_title.lower() in task["title"].lower():
                                            matched_task = task
                                            break

                                    if matched_task:
                                        actual_task_id = matched_task["id"]
                                        args = {"task_id": actual_task_id}
                                        result = self.execute_tool("complete_task", args, user_id)

                                        response_content = result.get("message", f"Task '{task_title}' {'marked as complete!' if result.get('success') else 'could not be completed.'}")

                                        tool_calls = [{
                                            "tool_name": "complete_task",
                                            "parameters": args,
                                            "result": result
                                        }]
                                        print(f"DEBUG: Complete by title operation executed, success: {result.get('success')}")
                                        break
                                    else:
                                        response_content = f"No task found with title containing '{task_title}'. Available tasks: {[t['title'] for t in tasks]}"
                                        tool_calls = []
                                        break
                                else:
                                    print(f"DEBUG: list_tasks failed when trying to complete by title: {list_result}")
                                    response_content = f"Could not find task with title '{task_title}' to complete."
                                    tool_calls = []
                                    break

            except Exception as gemini_error:
                error_str = str(gemini_error)
                logger.error(f"Gemini API error: {error_str}")
                print(f"ERROR: Gemini API failed: {error_str}")
                import traceback
                print(f"TRACEBACK: {traceback.format_exc()}")

                # Check if it's a rate limit error
                if "quota" in error_str.lower() or "rate" in error_str.lower() or "429" in error_str or "limit" in error_str.lower():
                    return {
                        "conversation_id": conversation_uuid,
                        "response": "I've reached my API usage limit. Please wait a moment before sending more requests.",
                        "tool_calls": [],
                        "timestamp": self.get_current_timestamp(),
                        "error": "Rate limit exceeded"
                    }
                elif "invalid argument" in error_str.lower() or "400" in error_str:
                    # Complete fallback response
                    return {
                        "conversation_id": conversation_uuid,
                        "response": "I'm having trouble processing your request right now. Could you please try rephrasing?",
                        "tool_calls": [],
                        "timestamp": self.get_current_timestamp(),
                        "error": "Invalid argument error"
                    }
                else:
                    # For other errors including rate limits, try to parse the user input directly
                    print(f"DEBUG: Attempting to parse user input directly due to error: {error_str}")

                    # Try to extract commands from the original user input
                    import re

                    # Check for delete command in user input
                    delete_patterns = [
                        r'delete\s+(\d+)',
                        r'delete.*?(\d+)',
                        r'remove.*?(\d+)',
                        r'task.*?(\d+).*?delete'
                    ]

                    for pattern in delete_patterns:
                        delete_match = re.search(pattern, user_input, re.IGNORECASE)
                        if delete_match:
                            display_index = int(delete_match.group(1))

                            # Convert display index to actual database ID
                            actual_task_id = display_index
                            if hasattr(self, 'task_id_map') and conversation_uuid in self.task_id_map:
                                actual_task_id = self.task_id_map[conversation_uuid].get(display_index, display_index)

                            args = {"task_id": actual_task_id}
                            result = self.execute_tool("delete_task", args, user_id)

                            if result.get("success"):
                                return {
                                    "conversation_id": conversation_uuid,
                                    "response": f"Task {display_index} deleted successfully!",
                                    "tool_calls": [{"tool_name": "delete_task", "parameters": args, "result": result}],
                                    "timestamp": self.get_current_timestamp()
                                }
                            else:
                                return {
                                    "conversation_id": conversation_uuid,
                                    "response": f"Failed to delete task {display_index}. {result.get('message', '')}",
                                    "tool_calls": [],
                                    "timestamp": self.get_current_timestamp()
                                }

                    # Check for complete command in user input
                    complete_patterns = [
                        r'complete\s+(\d+)',
                        r'complete.*?(\d+)',
                        r'finish.*?(\d+)',
                        r'mark.*?(\d+).*?done'
                    ]

                    for pattern in complete_patterns:
                        complete_match = re.search(pattern, user_input, re.IGNORECASE)
                        if complete_match:
                            display_index = int(complete_match.group(1))

                            # Convert display index to actual database ID
                            actual_task_id = display_index
                            if hasattr(self, 'task_id_map') and conversation_uuid in self.task_id_map:
                                actual_task_id = self.task_id_map[conversation_uuid].get(display_index, display_index)

                            args = {"task_id": actual_task_id}
                            result = self.execute_tool("complete_task", args, user_id)

                            if result.get("success"):
                                return {
                                    "conversation_id": conversation_uuid,
                                    "response": f"Task {display_index} marked as complete!",
                                    "tool_calls": [{"tool_name": "complete_task", "parameters": args, "result": result}],
                                    "timestamp": self.get_current_timestamp()
                                }
                            else:
                                return {
                                    "conversation_id": conversation_uuid,
                                    "response": f"Failed to complete task {display_index}. {result.get('message', '')}",
                                    "tool_calls": [],
                                    "timestamp": self.get_current_timestamp()
                                }

                    # Check for add task in user input
                    if any(keyword in user_input.lower() for keyword in ['add task', 'create task', 'new task']):
                        # Try to extract task details from natural language
                        import re

                        # Simple pattern to extract task info from natural language
                        title_match = re.search(r'(?:add|create|new)\s+task\s+(.+?)(?:\s+with|\s+and|\s+priority|\s+due|\s+$)', user_input, re.IGNORECASE)
                        priority_match = re.search(r'(high|medium|low)\s+priority', user_input, re.IGNORECASE)

                        if title_match:
                            task_title = title_match.group(1).strip()

                            args = {"title": task_title}
                            if priority_match:
                                args["priority"] = priority_match.group(1)

                            result = self.execute_tool("add_task", args, user_id)

                            return {
                                "conversation_id": conversation_uuid,
                                "response": result.get("message", f"Task '{task_title}' created successfully!"),
                                "tool_calls": [{"tool_name": "add_task", "parameters": args, "result": result}],
                                "timestamp": self.get_current_timestamp()
                            }

                    # If we can't parse the command, return error
                    return {
                        "conversation_id": conversation_uuid,
                        "response": "I'm currently unable to process your request due to an API issue. Please try again later.",
                        "tool_calls": [],
                        "timestamp": self.get_current_timestamp(),
                        "error": error_str
                    }

            # At this point, response_content and tool_calls have been set by the structured prompting approach above
            # No need to process tool_calls separately since they were already executed

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
                    # Only include role and content - Gemini doesn't need tool_calls in history
                    formatted_msg = {
                        "role": msg.role.value,
                        "content": msg.content
                    }
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