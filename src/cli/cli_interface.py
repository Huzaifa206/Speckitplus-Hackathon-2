"""Command-line interface for the Todo application."""

from typing import List, Tuple, Optional
from src.services.todo_service import TodoService


class CLIInterface:
    """Command-line interface for handling user commands."""

    def __init__(self, todo_service: TodoService) -> None:
        """Initialize the CLI interface with a Todo service."""
        self.todo_service = todo_service

    def parse_command(self, command: str) -> Tuple[str, List[str]]:
        """Parse a command string into command name and arguments."""
        parts = command.strip().split()
        if not parts:
            return "", []

        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

        # Handle quoted arguments
        if '"' in command or "'" in command:
            # Re-parse to handle quoted strings
            args = self._parse_with_quotes(command)

        return cmd, args

    def _parse_with_quotes(self, command: str) -> List[str]:
        """Parse command with quoted arguments."""
        parts = []
        current_arg = ""
        in_quotes = False
        quote_char = None

        i = 0
        while i < len(command):
            char = command[i]

            if char in ['"', "'"] and not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
            elif char == " " and not in_quotes:
                if current_arg:
                    parts.append(current_arg.strip())
                    current_arg = ""
            else:
                current_arg += char

            i += 1

        if current_arg:
            parts.append(current_arg.strip())

        # Remove the command part (first element)
        if parts:
            parts = parts[1:]  # Skip the command name (add, list, etc.)

        return parts

    def execute_command(self, command: str) -> str:
        """Execute a parsed command and return the result message."""
        cmd, args = self.parse_command(command)

        if cmd in ["add"]:
            return self._handle_add(args)
        elif cmd in ["list", "view"]:
            return self._handle_list()
        elif cmd in ["update"]:
            return self._handle_update(args)
        elif cmd in ["delete"]:
            return self._handle_delete(args)
        elif cmd in ["complete"]:
            return self._handle_complete(args)
        elif cmd in ["exit", "quit"]:
            return "exit"
        elif cmd in ["help", "?"]:
            return self._handle_help()
        else:
            return f"Unknown command: {cmd}. Type 'help' for available commands."

    def _handle_add(self, args: List[str]) -> str:
        """Handle the add command."""
        if len(args) == 0:
            return "Please provide a todo item to add. Usage: add \"todo text\""

        title = " ".join(args)
        if title.startswith('"') and title.endswith('"'):
            title = title[1:-1]
        elif title.startswith("'") and title.endswith("'"):
            title = title[1:-1]

        try:
            todo = self.todo_service.add_todo(title)
            return f"Added todo: \"{todo.title}\" (ID: {todo.id})"
        except ValueError as e:
            return f"Error adding todo: {str(e)}"

    def _handle_list(self) -> str:
        """Handle the list/view command."""
        todos = self.todo_service.get_all_todos()

        if not todos:
            return "No todos found."

        todo_list = []
        for todo in todos:
            todo_list.append(str(todo))

        return "\n".join(todo_list)

    def _handle_update(self, args: List[str]) -> str:
        """Handle the update command."""
        if len(args) < 2:
            return "Usage: update <id> \"new text\""

        try:
            todo_id = int(args[0])
        except ValueError:
            return f"Invalid ID: {args[0]}. ID must be a number."

        new_text = " ".join(args[1:])
        if new_text.startswith('"') and new_text.endswith('"'):
            new_text = new_text[1:-1]
        elif new_text.startswith("'") and new_text.endswith("'"):
            new_text = new_text[1:-1]

        if not new_text or not new_text.strip():
            return "New text cannot be empty or contain only whitespace."

        if not self.todo_service.validate_todo_id(todo_id):
            return f"Todo with ID {todo_id} does not exist."

        try:
            success = self.todo_service.update_todo(todo_id, new_text)
            if success:
                return f"Todo {todo_id} updated successfully."
            else:
                return f"Failed to update todo {todo_id}."
        except ValueError as e:
            return f"Error updating todo: {str(e)}"

    def _handle_delete(self, args: List[str]) -> str:
        """Handle the delete command."""
        if len(args) != 1:
            return "Usage: delete <id>"

        try:
            todo_id = int(args[0])
        except ValueError:
            return f"Invalid ID: {args[0]}. ID must be a number."

        if not self.todo_service.validate_todo_id(todo_id):
            return f"Todo with ID {todo_id} does not exist."

        success = self.todo_service.delete_todo(todo_id)
        if success:
            return f"Todo {todo_id} deleted successfully."
        else:
            return f"Failed to delete todo {todo_id}."

    def _handle_complete(self, args: List[str]) -> str:
        """Handle the complete command."""
        if len(args) != 1:
            return "Usage: complete <id>"

        try:
            todo_id = int(args[0])
        except ValueError:
            return f"Invalid ID: {args[0]}. ID must be a number."

        if not self.todo_service.validate_todo_id(todo_id):
            return f"Todo with ID {todo_id} does not exist."

        success = self.todo_service.mark_complete(todo_id)
        if success:
            return f"Todo {todo_id} marked as complete."
        else:
            return f"Failed to mark todo {todo_id} as complete."

    def _handle_help(self) -> str:
        """Handle the help command."""
        help_text = """
Available commands:
  add "text"        - Add a new todo item
  list/view         - List all todo items
  update <id> "text" - Update a todo item
  delete <id>       - Delete a todo item
  complete <id>     - Mark a todo as complete
  help/?            - Show this help message
  exit/quit         - Exit the application
        """.strip()
        return help_text