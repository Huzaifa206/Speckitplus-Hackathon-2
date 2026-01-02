"""Main entry point for the Console Todo App."""

from src.repositories.todo_repository import TodoRepository
from src.services.todo_service import TodoService
from src.cli.cli_interface import CLIInterface


def main():
    """Main function to run the Console Todo App."""
    print("Welcome to the Console Todo App!")
    print('Available commands:\n'
    'add "text"        - Add a new todo item\n'
    'list/view         - List all todo items\n'
    'update <id> "text" - Update a todo item\n'
    'delete <id>       - Delete a todo item\n'
    'complete <id>     - Mark a todo as complete\n'
    'help/?            - Show this help message\n'
    'exit/quit         - Exit the application'
)

    # Initialize the application components
    repository = TodoRepository()
    service = TodoService(repository)
    cli = CLIInterface(service)

    # Main REPL loop
    while True:
        try:
            command = input("> ").strip()

            if not command:
                continue

            result = cli.execute_command(command)

            if result == "exit":
                print("Goodbye!")
                break
            else:
                print(result)

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()