"""Business logic service for Todo operations."""

from typing import List, Optional
from src.models.todo import Todo
from src.repositories.todo_repository import TodoRepository


class TodoService:
    """Business logic layer for Todo operations."""

    def __init__(self, repository: TodoRepository) -> None:
        """Initialize the service with a repository."""
        self.repository = repository

    def add_todo(self, title: str) -> Todo:
        """Add a new todo item with validation."""
        # Input validation is handled in the repository and model
        return self.repository.add_todo(title)

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """Get a todo item by its ID."""
        return self.repository.get_todo_by_id(todo_id)

    def get_all_todos(self) -> List[Todo]:
        """Get all todo items."""
        return self.repository.get_all_todos()

    def update_todo(self, todo_id: int, new_title: str) -> bool:
        """Update the title of an existing todo item."""
        updated_todo = self.repository.update_todo(todo_id, new_title)
        return updated_todo is not None

    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo item by ID."""
        return self.repository.delete_todo(todo_id)

    def mark_complete(self, todo_id: int) -> bool:
        """Mark a todo item as complete."""
        todo = self.repository.mark_complete(todo_id)
        return todo is not None

    def mark_incomplete(self, todo_id: int) -> bool:
        """Mark a todo item as incomplete."""
        todo = self.repository.mark_incomplete(todo_id)
        return todo is not None

    def validate_todo_id(self, todo_id: int) -> bool:
        """Check if a todo ID exists in the repository."""
        return self.repository.get_todo_by_id(todo_id) is not None