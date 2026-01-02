# API Contracts: Console Todo App

## Todo Operations

### Add Todo
- **Command**: `add "todo text"`
- **Input**: Todo text as string
- **Output**: Success message with assigned ID
- **Error Cases**: Empty todo text

### List Todos
- **Command**: `list` or `view`
- **Input**: None
- **Output**: Formatted list of todos with IDs and completion status
- **Error Cases**: None (empty list if no todos)

### Update Todo
- **Command**: `update {id} "new text"`
- **Input**: Todo ID (int) and new text (string)
- **Output**: Success message
- **Error Cases**: Invalid ID, empty text

### Delete Todo
- **Command**: `delete {id}`
- **Input**: Todo ID (int)
- **Output**: Success message
- **Error Cases**: Invalid ID

### Mark Complete
- **Command**: `complete {id}`
- **Input**: Todo ID (int)
- **Output**: Success message
- **Error Cases**: Invalid ID

### Exit
- **Command**: `exit`
- **Input**: None
- **Output**: Exit message
- **Error Cases**: None