# Data Model: Console Todo App

## Todo Entity

### Fields
- **id** (int): Unique identifier for the todo item, auto-incremented
- **title** (str): Text content of the todo item, required
- **completed** (bool): Completion status, default false

### Validation Rules
- Title must not be empty or contain only whitespace
- ID must be unique within the todo list
- ID must be positive integer

### State Transitions
- **Incomplete → Complete**: When mark complete operation is performed
- **Complete → Incomplete**: When mark incomplete operation is performed (if supported)

## TodoList Collection

### Structure
- **items** (list): Collection of Todo entities stored in memory
- **next_id** (int): Counter for auto-generating unique IDs

### Operations
- Add new todo item
- Get todo item by ID
- Update todo item by ID
- Delete todo item by ID
- List all todo items
- Mark todo item as complete/incomplete