"""Integration tests for the CLI functionality."""

import io
import sys
from contextlib import redirect_stdout, redirect_stderr
from src.repositories.todo_repository import TodoRepository
from src.services.todo_service import TodoService
from src.cli.cli_interface import CLIInterface


def test_cli_full_workflow():
    """Test the full workflow through the CLI interface."""
    # Initialize the application components
    repository = TodoRepository()
    service = TodoService(repository)
    cli = CLIInterface(service)

    # Test adding a todo
    result = cli.execute_command('add "Buy groceries"')
    assert "Added todo: \"Buy groceries\" (ID: 1)" in result

    # Test adding another todo
    result = cli.execute_command('add "Walk the dog"')
    assert "Added todo: \"Walk the dog\" (ID: 2)" in result

    # Test listing todos
    result = cli.execute_command('list')
    assert "1. [ ] Buy groceries" in result
    assert "2. [ ] Walk the dog" in result

    # Test marking a todo as complete
    result = cli.execute_command('complete 1')
    assert "Todo 1 marked as complete" in result

    # Test listing todos again to see the updated status
    result = cli.execute_command('list')
    assert "1. [x] Buy groceries" in result
    assert "2. [ ] Walk the dog" in result

    # Test updating a todo
    result = cli.execute_command('update 2 "Walk the big dog"')
    assert "Todo 2 updated successfully" in result

    # Test listing todos to see the updated text
    result = cli.execute_command('list')
    assert "2. [ ] Walk the big dog" in result

    # Test deleting a todo
    result = cli.execute_command('delete 2')
    assert "Todo 2 deleted successfully" in result

    # Test listing todos to see that one was deleted
    result = cli.execute_command('list')
    assert "1. [x] Buy groceries" in result
    assert "2. [ ] Walk the big dog" not in result
    assert len(result.splitlines()) == 1  # Only one todo should remain


def test_cli_error_handling():
    """Test CLI error handling for invalid inputs."""
    repository = TodoRepository()
    service = TodoService(repository)
    cli = CLIInterface(service)

    # Test adding empty todo
    result = cli.execute_command('add ""')
    assert "Error adding todo" in result

    # Test adding todo with only whitespace
    result = cli.execute_command('add "   "')
    assert "Error adding todo" in result

    # Test updating non-existent todo
    result = cli.execute_command('update 999 "New title"')
    assert "does not exist" in result

    # Test deleting non-existent todo
    result = cli.execute_command('delete 999')
    assert "does not exist" in result

    # Test marking non-existent todo as complete
    result = cli.execute_command('complete 999')
    assert "does not exist" in result

    # Test invalid ID for operations
    result = cli.execute_command('complete abc')
    assert "Invalid ID" in result

    result = cli.execute_command('update abc "new text"')
    assert "Invalid ID" in result

    result = cli.execute_command('delete xyz')
    assert "Invalid ID" in result


def test_cli_help_command():
    """Test the help command."""
    repository = TodoRepository()
    service = TodoService(repository)
    cli = CLIInterface(service)

    result = cli.execute_command('help')
    assert "Available commands" in result
    assert "add" in result
    assert "list" in result
    assert "update" in result
    assert "delete" in result
    assert "complete" in result


def test_cli_empty_list():
    """Test listing when there are no todos."""
    repository = TodoRepository()
    service = TodoService(repository)
    cli = CLIInterface(service)

    result = cli.execute_command('list')
    assert "No todos found" in result


def test_cli_view_command():
    """Test that 'view' command works the same as 'list'."""
    repository = TodoRepository()
    service = TodoService(repository)
    cli = CLIInterface(service)

    # Add a todo first
    cli.execute_command('add "Test todo"')

    # Test both commands give same result
    list_result = cli.execute_command('list')
    view_result = cli.execute_command('view')

    assert list_result == view_result
    assert "Test todo" in list_result