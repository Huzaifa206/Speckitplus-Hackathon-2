"""Unit tests for the TodoService."""

import pytest
from src.models.todo import Todo
from src.repositories.todo_repository import TodoRepository
from src.services.todo_service import TodoService


def test_service_initialization():
    """Test initializing the service with a repository."""
    repo = TodoRepository()
    service = TodoService(repo)

    assert service.repository == repo


def test_add_todo():
    """Test adding a todo through the service."""
    repo = TodoRepository()
    service = TodoService(repo)

    todo = service.add_todo("Test todo")

    assert todo.id == 1
    assert todo.title == "Test todo"
    assert todo.completed is False

    # Verify it's in the repository
    retrieved_todo = service.get_todo_by_id(1)
    assert retrieved_todo is not None
    assert retrieved_todo.title == "Test todo"


def test_get_todo_by_id():
    """Test getting a todo by ID through the service."""
    repo = TodoRepository()
    service = TodoService(repo)
    added_todo = service.add_todo("Test todo")

    retrieved_todo = service.get_todo_by_id(1)
    assert retrieved_todo is not None
    assert retrieved_todo.id == 1
    assert retrieved_todo.title == "Test todo"

    nonexistent_todo = service.get_todo_by_id(999)
    assert nonexistent_todo is None


def test_get_all_todos():
    """Test getting all todos through the service."""
    repo = TodoRepository()
    service = TodoService(repo)
    service.add_todo("First todo")
    service.add_todo("Second todo")

    todos = service.get_all_todos()
    assert len(todos) == 2


def test_update_todo():
    """Test updating a todo through the service."""
    repo = TodoRepository()
    service = TodoService(repo)
    service.add_todo("Original title")

    success = service.update_todo(1, "Updated title")
    assert success is True

    # Verify the change
    updated_todo = service.get_todo_by_id(1)
    assert updated_todo is not None
    assert updated_todo.title == "Updated title"


def test_update_nonexistent_todo():
    """Test updating a non-existent todo."""
    repo = TodoRepository()
    service = TodoService(repo)

    success = service.update_todo(999, "New title")
    assert success is False


def test_delete_todo():
    """Test deleting a todo through the service."""
    repo = TodoRepository()
    service = TodoService(repo)
    service.add_todo("Test todo")

    success = service.delete_todo(1)
    assert success is True

    # Verify it's gone
    todos = service.get_all_todos()
    assert len(todos) == 0

    retrieved_todo = service.get_todo_by_id(1)
    assert retrieved_todo is None


def test_delete_nonexistent_todo():
    """Test deleting a non-existent todo."""
    repo = TodoRepository()
    service = TodoService(repo)

    success = service.delete_todo(999)
    assert success is False


def test_mark_complete():
    """Test marking a todo as complete through the service."""
    repo = TodoRepository()
    service = TodoService(repo)
    service.add_todo("Test todo")

    success = service.mark_complete(1)
    assert success is True

    # Verify the change
    todo = service.get_todo_by_id(1)
    assert todo is not None
    assert todo.completed is True


def test_mark_incomplete():
    """Test marking a todo as incomplete through the service."""
    repo = TodoRepository()
    service = TodoService(repo)
    service.add_todo("Test todo")
    service.mark_complete(1)  # Mark as complete first

    success = service.mark_incomplete(1)
    assert success is True

    # Verify the change
    todo = service.get_todo_by_id(1)
    assert todo is not None
    assert todo.completed is False


def test_mark_nonexistent_todo():
    """Test marking a non-existent todo."""
    repo = TodoRepository()
    service = TodoService(repo)

    success = service.mark_complete(999)
    assert success is False

    success = service.mark_incomplete(999)
    assert success is False


def test_validate_todo_id():
    """Test validating a todo ID."""
    repo = TodoRepository()
    service = TodoService(repo)
    service.add_todo("Test todo")

    assert service.validate_todo_id(1) is True
    assert service.validate_todo_id(999) is False