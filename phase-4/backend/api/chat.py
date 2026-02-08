"""
Chat API endpoints for the Gemini-powered chatbot
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from sqlmodel import Session
from typing import Optional
import logging
from core.database import get_session
from models.message import Message
from models.conversation import Conversation
from pydantic import BaseModel
from agent import process_user_message

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up rate limiting
limiter = Limiter(key_func=get_remote_address)
router = APIRouter(prefix="/chat", tags=["chat"])

# Add rate limit exception handler
def add_rate_limit_exception_handler(app):
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


class ChatRequest(BaseModel):
    user_input: str
    conversation_id: Optional[str] = None
    user_id: str = "default_user"  # In a real app, this would come from authentication


class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    tool_calls: list
    timestamp: str


@router.post("/", response_model=ChatResponse)
@limiter.limit("10/minute")
async def chat_endpoint(request: Request, chat_request: ChatRequest):
    """
    Process user input and return AI response with potential tool execution
    """
    try:
        print(f"DEBUG: Chat endpoint received user_id: {chat_request.user_id}")
        result = process_user_message(
            user_input=chat_request.user_input,
            user_id=chat_request.user_id,
            conversation_id=chat_request.conversation_id
        )

        if "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result["error"]
            )

        return ChatResponse(
            conversation_id=result["conversation_id"],
            response=result["response"],
            tool_calls=result["tool_calls"],
            timestamp=result["timestamp"]
        )
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while processing your request: {str(e)}"
        )


class GetConversationsResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str
    is_active: bool


@router.get("/conversations", response_model=list[GetConversationsResponse])
@limiter.limit("20/minute")
async def get_conversations(request: Request, user_id: str = "default_user"):
    """
    Retrieve list of user's conversations
    """
    try:
        from sqlmodel import select
        from core.database import get_db_session
        from models.conversation import Conversation
        from datetime import datetime

        with get_db_session() as session:
            statement = select(Conversation).where(Conversation.user_id == user_id)
            conversations = session.exec(statement).all()

            result = []
            for conv in conversations:
                result.append(GetConversationsResponse(
                    id=conv.uuid,
                    title=conv.title,
                    created_at=conv.created_at.isoformat() if conv.created_at else "",
                    updated_at=conv.updated_at.isoformat() if conv.updated_at else "",
                    is_active=conv.is_active
                ))

            return result
    except Exception as e:
        logger.error(f"Error retrieving conversations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving conversations: {str(e)}"
        )


class GetMessageResponse(BaseModel):
    id: int
    role: str
    content: str
    timestamp: str
    tool_calls: Optional[list] = None


@router.get("/conversations/{conversation_id}/messages", response_model=list[GetMessageResponse])
@limiter.limit("30/minute")
async def get_conversation_messages(request: Request, conversation_id: str, user_id: str = "default_user"):
    """
    Retrieve messages for a specific conversation
    """
    try:
        from sqlmodel import select
        from core.database import get_db_session
        from models.message import Message
        import json

        with get_db_session() as session:
            # First, get the conversation to ensure it belongs to the user
            from models.conversation import Conversation as Conv
            conv_statement = select(Conv).where(Conv.uuid == conversation_id)
            conversation = session.exec(conv_statement).first()

            if not conversation or conversation.user_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found or doesn't belong to user"
                )

            # Get messages for this conversation
            message_statement = select(Message).where(
                Message.conversation_id == conversation.id
            ).order_by(Message.created_at)
            messages = session.exec(message_statement).all()

            result = []
            for msg in messages:
                tool_calls_data = None
                if msg.tool_calls:
                    try:
                        tool_calls_data = json.loads(msg.tool_calls)
                    except:
                        tool_calls_data = None

                result.append(GetMessageResponse(
                    id=msg.id,
                    role=msg.role.value,
                    content=msg.content,
                    timestamp=msg.created_at.isoformat() if msg.created_at else "",
                    tool_calls=tool_calls_data
                ))

            return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving conversation messages: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving conversation messages: {str(e)}"
        )