# Console Todo App

A Phase I In-Memory Python Console Todo App implementing Add, View, Update, Delete, and Mark Complete operations using in-memory storage. The application follows a clean architecture with separation of concerns, including domain models, services layer, and CLI interface.

## Prerequisites

- Python 3.13+
- UV package manager

## Setup

1. Clone the repository
2. Navigate to project directory
3. Install dependencies: `uv sync`
4. Run the application: `python -m src.main`

## Usage

The application starts in an interactive command loop. Available commands:

### Add Todo
```
add "Buy groceries"
```

### List Todos
```
list
```
or
```
view
```

### Update Todo
```
update 1 "Buy groceries and cook dinner"
```

### Delete Todo
```
delete 1
```

### Mark Complete
```
complete 1
```

### Exit Application
```
exit
```

## Example Session
```
> add "Buy milk"
Added todo: "Buy milk" (ID: 1)
> add "Walk the dog"
Added todo: "Walk the dog" (ID: 2)
> list
1. [ ] Buy milk
2. [ ] Walk the dog
> complete 1
Todo 1 marked as complete
> list
1. [x] Buy milk
2. [ ] Walk the dog
> exit
Goodbye!
```

## Development

- Run tests: `uv run pytest`
- Run application: `uv run python -m src.main`