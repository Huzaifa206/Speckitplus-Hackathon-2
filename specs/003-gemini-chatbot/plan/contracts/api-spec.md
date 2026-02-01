# API Contracts: Phase III - Gemini-Powered Chatbot

## Chat API

### POST /api/chat
**Description**: Process user input and return AI response with potential tool execution

**Request**:
```json
{
  "user_input": "Add a task to buy groceries",
  "conversation_id": "optional-existing-conversation-id",
  "user_id": "authenticated-user-id"
}
```

**Response**:
```json
{
  "conversation_id": "new-or-existing-conversation-id",
  "response": "I've created a task to buy groceries for you.",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "parameters": {
        "title": "Buy groceries",
        "priority": "medium"
      },
      "result": {
        "success": true,
        "task_id": 123
      }
    }
  ],
  "timestamp": "2026-02-01T10:00:00Z"
}
```

**Error Responses**:
- 400: Invalid request format
- 401: Unauthorized access
- 429: Rate limit exceeded
- 500: Internal server error (e.g., Gemini API unavailable)

### GET /api/conversations
**Description**: Retrieve list of user's conversations

**Query Parameters**:
- `limit`: Number of conversations to return (default: 10)
- `offset`: Number of conversations to skip (default: 0)
- `sort_by`: Field to sort by (created_at, updated_at) (default: updated_at)

**Response**:
```json
[
  {
    "id": "conversation-uuid",
    "title": "Task management session",
    "created_at": "2026-02-01T09:00:00Z",
    "updated_at": "2026-02-01T10:00:00Z",
    "is_active": true
  }
]
```

### GET /api/conversations/{conversation_id}/messages
**Description**: Retrieve messages for a specific conversation

**Response**:
```json
[
  {
    "id": 1,
    "role": "user",
    "content": "Add a task to buy groceries",
    "timestamp": "2026-02-01T09:30:00Z"
  },
  {
    "id": 2,
    "role": "assistant",
    "content": "I've created a task to buy groceries for you.",
    "timestamp": "2026-02-01T09:30:05Z",
    "tool_calls": [
      {
        "tool_name": "add_task",
        "parameters": {"title": "Buy groceries"},
        "result": {"success": true, "task_id": 123}
      }
    ]
  }
]
```

## MCP Tool Contracts

### Tool: add_task
**Description**: Create a new task for the user

**Parameters**:
```json
{
  "title": "Task title",
  "description": "Optional description",
  "priority": "high|medium|low",
  "due_date": "Optional ISO date string",
  "tags": ["optional", "tag", "array"]
}
```

**Response**:
```json
{
  "success": true,
  "task_id": 123,
  "message": "Task created successfully"
}
```

### Tool: list_tasks
**Description**: Retrieve user's tasks with optional filtering

**Parameters**:
```json
{
  "status": "all|completed|pending",
  "priority": "all|high|medium|low",
  "search": "Optional search term",
  "limit": "Optional limit",
  "offset": "Optional offset"
}
```

**Response**:
```json
{
  "success": true,
  "tasks": [
    {
      "id": 123,
      "title": "Task title",
      "description": "Task description",
      "completed": false,
      "priority": "high",
      "due_date": "2026-12-31T10:00:00Z",
      "tags": ["tag1", "tag2"]
    }
  ],
  "total_count": 1
}
```

### Tool: complete_task
**Description**: Mark a task as completed

**Parameters**:
```json
{
  "task_id": 123
}
```

**Response**:
```json
{
  "success": true,
  "message": "Task marked as completed"
}
```

### Tool: delete_task
**Description**: Remove a task

**Parameters**:
```json
{
  "task_id": 123
}
```

**Response**:
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```