"""Custom error classes for the Console Todo App."""


class TodoError(Exception):
    """Base exception for todo-related errors."""
    pass


class TodoNotFoundError(TodoError):
    """Raised when a requested todo item is not found."""
    pass


class InvalidTodoTitleError(TodoError):
    """Raised when a todo title is invalid (empty or whitespace)."""
    pass


class InvalidTodoIdError(TodoError):
    """Raised when a todo ID is invalid (not positive integer)."""
    pass


class TodoOperationError(TodoError):
    """Raised when a todo operation fails."""
    pass