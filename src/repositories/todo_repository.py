"""In-memory repository for managing Todo items."""

from typing import Dict, List, Optional
from src.models.todo import Todo


class TodoRepository:
    """In-memory storage layer for Todo items using Python dictionary and list structures."""

    def __init__(self) -> None:
        """Initialize the repository with an empty collection of todos and ID counter."""
        self._todos: Dict[int, Todo] = {}
        self._next_id: int = 1

    def add_todo(self, title: str) -> Todo:
        """Add a new todo item with the given title and return the created Todo object."""
        # Validate input
        if not title or not title.strip():
            raise ValueError("Todo title cannot be empty or contain only whitespace")

        # Create new todo with unique ID
        todo = Todo(id=self._next_id, title=title.strip())
        self._todos[todo.id] = todo

        # Increment the next ID for the next todo
        self._next_id += 1

        return todo

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """Get a todo item by its ID, or None if not found."""
        return self._todos.get(todo_id)

    def get_all_todos(self) -> List[Todo]:
        """Get all todo items in the repository."""
        return list(self._todos.values())

    def update_todo(self, todo_id: int, new_title: str) -> Optional[Todo]:
        """Update the title of an existing todo item by ID."""
        if not new_title or not new_title.strip():
            raise ValueError("Todo title cannot be empty or contain only whitespace")

        todo = self._todos.get(todo_id)
        if todo:
            todo.update_title(new_title)
            return todo
        return None

    def delete_todo(self, todo_id: int) -> bool:
        """Delete a todo item by ID and return True if successful."""
        if todo_id in self._todos:
            del self._todos[todo_id]
            return True
        return False

    def mark_complete(self, todo_id: int) -> Optional[Todo]:
        """Mark a todo item as complete by ID."""
        todo = self._todos.get(todo_id)
        if todo:
            todo.mark_complete()
            return todo
        return None

    def mark_incomplete(self, todo_id: int) -> Optional[Todo]:
        """Mark a todo item as incomplete by ID."""
        todo = self._todos.get(todo_id)
        if todo:
            todo.mark_incomplete()
            return todo
        return None

    def get_next_id(self) -> int:
        """Get the next available ID for a new todo."""
        return self._next_id