"""Unit tests for the Todo model."""

import pytest
from src.models.todo import Todo


def test_todo_creation():
    """Test creating a valid Todo item."""
    todo = Todo(id=1, title="Test todo")
    assert todo.id == 1
    assert todo.title == "Test todo"
    assert todo.completed is False


def test_todo_creation_with_completion_status():
    """Test creating a Todo item with completion status."""
    todo = Todo(id=1, title="Test todo", completed=True)
    assert todo.id == 1
    assert todo.title == "Test todo"
    assert todo.completed is True


def test_todo_mark_complete():
    """Test marking a Todo item as complete."""
    todo = Todo(id=1, title="Test todo")
    assert todo.completed is False
    todo.mark_complete()
    assert todo.completed is True


def test_todo_mark_incomplete():
    """Test marking a Todo item as incomplete."""
    todo = Todo(id=1, title="Test todo", completed=True)
    assert todo.completed is True
    todo.mark_incomplete()
    assert todo.completed is False


def test_todo_update_title():
    """Test updating a Todo item's title."""
    todo = Todo(id=1, title="Old title")
    assert todo.title == "Old title"
    todo.update_title("New title")
    assert todo.title == "New title"


def test_todo_str_representation():
    """Test the string representation of a Todo item."""
    todo = Todo(id=1, title="Test todo")
    assert str(todo) == "1. [ ] Test todo"

    todo.mark_complete()
    assert str(todo) == "1. [x] Test todo"


def test_todo_invalid_title():
    """Test creating a Todo item with invalid title."""
    with pytest.raises(ValueError):
        Todo(id=1, title="")

    with pytest.raises(ValueError):
        Todo(id=1, title="   ")

    with pytest.raises(ValueError):
        Todo(id=1, title="\t\n")


def test_todo_invalid_id():
    """Test creating a Todo item with invalid ID."""
    with pytest.raises(ValueError):
        Todo(id=0, title="Test todo")

    with pytest.raises(ValueError):
        Todo(id=-1, title="Test todo")


def test_todo_update_title_validation():
    """Test updating a Todo item's title with invalid input."""
    todo = Todo(id=1, title="Valid title")

    with pytest.raises(ValueError):
        todo.update_title("")

    with pytest.raises(ValueError):
        todo.update_title("   ")

    with pytest.raises(ValueError):
        todo.update_title("\t\n")