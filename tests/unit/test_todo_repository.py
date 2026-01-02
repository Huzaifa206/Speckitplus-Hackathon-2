"""Unit tests for the TodoRepository."""

import pytest
from src.models.todo import Todo
from src.repositories.todo_repository import TodoRepository


def test_repository_initialization():
    """Test initializing an empty repository."""
    repo = TodoRepository()
    assert len(repo.get_all_todos()) == 0
    assert repo.get_next_id() == 1


def test_add_todo():
    """Test adding a todo to the repository."""
    repo = TodoRepository()
    todo = repo.add_todo("Test todo")

    assert todo.id == 1
    assert todo.title == "Test todo"
    assert todo.completed is False

    todos = repo.get_all_todos()
    assert len(todos) == 1
    assert todos[0].id == 1
    assert todos[0].title == "Test todo"


def test_add_todo_with_next_id():
    """Test that IDs are assigned sequentially."""
    repo = TodoRepository()
    todo1 = repo.add_todo("First todo")
    todo2 = repo.add_todo("Second todo")

    assert todo1.id == 1
    assert todo2.id == 2
    assert repo.get_next_id() == 3


def test_add_todo_empty_title():
    """Test adding a todo with empty title raises an error."""
    repo = TodoRepository()

    with pytest.raises(ValueError):
        repo.add_todo("")

    with pytest.raises(ValueError):
        repo.add_todo("   ")


def test_get_todo_by_id():
    """Test getting a todo by ID."""
    repo = TodoRepository()
    added_todo = repo.add_todo("Test todo")

    retrieved_todo = repo.get_todo_by_id(1)
    assert retrieved_todo is not None
    assert retrieved_todo.id == 1
    assert retrieved_todo.title == "Test todo"

    nonexistent_todo = repo.get_todo_by_id(999)
    assert nonexistent_todo is None


def test_get_all_todos():
    """Test getting all todos."""
    repo = TodoRepository()
    todo1 = repo.add_todo("First todo")
    todo2 = repo.add_todo("Second todo")

    todos = repo.get_all_todos()
    assert len(todos) == 2
    assert todos[0].id == 1
    assert todos[1].id == 2


def test_update_todo():
    """Test updating a todo's title."""
    repo = TodoRepository()
    original_todo = repo.add_todo("Original title")

    updated_todo = repo.update_todo(1, "Updated title")
    assert updated_todo is not None
    assert updated_todo.id == 1
    assert updated_todo.title == "Updated title"

    # Verify the change is reflected in the repository
    retrieved_todo = repo.get_todo_by_id(1)
    assert retrieved_todo.title == "Updated title"


def test_update_todo_empty_title():
    """Test updating a todo with empty title raises an error."""
    repo = TodoRepository()
    repo.add_todo("Original title")

    result = repo.update_todo(1, "")
    assert result is None

    result = repo.update_todo(1, "   ")
    assert result is None


def test_update_nonexistent_todo():
    """Test updating a non-existent todo."""
    repo = TodoRepository()
    result = repo.update_todo(999, "New title")
    assert result is None


def test_delete_todo():
    """Test deleting a todo."""
    repo = TodoRepository()
    repo.add_todo("Test todo")

    success = repo.delete_todo(1)
    assert success is True

    todos = repo.get_all_todos()
    assert len(todos) == 0

    retrieved_todo = repo.get_todo_by_id(1)
    assert retrieved_todo is None


def test_delete_nonexistent_todo():
    """Test deleting a non-existent todo."""
    repo = TodoRepository()
    success = repo.delete_todo(999)
    assert success is False


def test_mark_complete():
    """Test marking a todo as complete."""
    repo = TodoRepository()
    todo = repo.add_todo("Test todo")
    assert todo.completed is False

    marked_todo = repo.mark_complete(1)
    assert marked_todo is not None
    assert marked_todo.completed is True

    # Verify the change is reflected in the repository
    retrieved_todo = repo.get_todo_by_id(1)
    assert retrieved_todo.completed is True


def test_mark_incomplete():
    """Test marking a todo as incomplete."""
    repo = TodoRepository()
    todo = repo.add_todo("Test todo")
    todo.mark_complete()  # Mark as complete first
    assert todo.completed is True

    marked_todo = repo.mark_incomplete(1)
    assert marked_todo is not None
    assert marked_todo.completed is False

    # Verify the change is reflected in the repository
    retrieved_todo = repo.get_todo_by_id(1)
    assert retrieved_todo.completed is False


def test_mark_nonexistent_todo():
    """Test marking a non-existent todo."""
    repo = TodoRepository()
    result = repo.mark_complete(999)
    assert result is None

    result = repo.mark_incomplete(999)
    assert result is None