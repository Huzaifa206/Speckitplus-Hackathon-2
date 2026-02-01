"""
Logging configuration for Phase 3 - Gemini-Powered Chatbot
"""
import logging
import sys
from datetime import datetime
from typing import Optional


class ChatLogger:
    """Logger for chat interactions"""

    def __init__(self, name: str = "chatbot"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Prevent adding multiple handlers if logger already exists
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_interaction(self, user_id: str, conversation_id: str, user_input: str, ai_response: str):
        """Log a chat interaction"""
        self.logger.info(f"Interaction - User: {user_id}, Conv: {conversation_id[:8]}..., Input: {user_input[:50]}...")

    def log_tool_execution(self, user_id: str, conversation_id: str, tool_name: str, parameters: dict, result: dict):
        """Log a tool execution"""
        self.logger.info(f"Tool Execution - User: {user_id}, Conv: {conversation_id[:8]}..., Tool: {tool_name}")

    def log_error(self, user_id: Optional[str], error: Exception, context: str = ""):
        """Log an error"""
        self.logger.error(f"Error - User: {user_id or 'unknown'}, Context: {context}, Error: {str(error)}")


# Global logger instance
chat_logger = ChatLogger()


def get_chat_logger():
    """Get the global chat logger instance"""
    return chat_logger