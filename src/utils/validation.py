"""Validation utilities for the Console Todo App."""


def validate_todo_title(title: str) -> bool:
    """Validate that a todo title is not empty or whitespace only."""
    if not title:
        return False
    if not title.strip():
        return False
    return True


def validate_todo_id(todo_id: int) -> bool:
    """Validate that a todo ID is a positive integer."""
    if not isinstance(todo_id, int):
        return False
    if todo_id <= 0:
        return False
    return True


def validate_non_empty_string(value: str) -> bool:
    """Validate that a string is not empty or whitespace only."""
    if not value:
        return False
    if not value.strip():
        return False
    return True