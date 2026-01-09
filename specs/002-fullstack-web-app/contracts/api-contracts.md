# API Contracts: Full-Stack Web Application

## Authentication API

### POST /api/auth/login
- **Purpose**: Authenticate user and return JWT token
- **Request**:
  ```json
  {
    "email": "string (required)",
    "password": "string (required)"
  }
  ```
- **Response (200)**:
  ```json
  {
    "access_token": "string (JWT token)",
    "token_type": "string (default: 'bearer')",
    "user": {
      "id": "string (user ID)",
      "email": "string (user email)",
      "name": "string (user name)"
    }
  }
  ```
- **Errors**: 400 (Invalid credentials), 422 (Validation error)

### POST /api/auth/register
- **Purpose**: Register a new user
- **Request**:
  ```json
  {
    "email": "string (required, valid email)",
    "password": "string (required, min 8 chars)",
    "name": "string (required)"
  }
  ```
- **Response (201)**:
  ```json
  {
    "id": "string (user ID)",
    "email": "string (user email)",
    "name": "string (user name)"
  }
  ```
- **Errors**: 400 (Email already exists), 422 (Validation error)

## Task API

### GET /api/{user_id}/tasks
- **Purpose**: Retrieve user's tasks with optional filtering and sorting
- **Headers**: Authorization: Bearer {token}
- **Query Parameters**:
  - `search` (optional): Keyword search in title/description
  - `priority` (optional): "high", "medium", "low" (filter by priority)
  - `sort` (optional): "due_date", "priority", "title", "created_at" (sorting field)
  - `order` (optional): "asc" or "desc" (default: asc)
  - `limit` (optional): Number of results to return
  - `offset` (optional): Offset for pagination
- **Response (200)**:
  ```json
  {
    "tasks": [
      {
        "id": "integer (task ID)",
        "user_id": "string (user ID)",
        "title": "string (task title)",
        "description": "string (task description)",
        "completed": "boolean (completion status)",
        "priority": "string (high/medium/low)",
        "tags": ["string (tag names)"],
        "due_date": "string (ISO 8601 date, optional)",
        "is_recurring": "boolean (recurring flag)",
        "recurring_interval": "string (daily/weekly, optional)",
        "created_at": "string (ISO 8601 datetime)"
      }
    ],
    "total": "integer (total count for pagination)"
  }
  ```
- **Errors**: 401 (Unauthorized), 403 (Forbidden - wrong user ID)

### POST /api/{user_id}/tasks
- **Purpose**: Create a new task for the specified user
- **Headers**: Authorization: Bearer {token}
- **Request**:
  ```json
  {
    "title": "string (required)",
    "description": "string (optional)",
    "completed": "boolean (default: false)",
    "priority": "string (enum: 'high', 'medium', 'low'; default: 'medium')",
    "tags": ["string (array of tag names, optional)"],
    "due_date": "string (ISO 8601 date format, optional)",
    "is_recurring": "boolean (default: false)",
    "recurring_interval": "string (enum: 'daily', 'weekly', null; optional)"
  }
  ```
- **Response (201)**:
  ```json
  {
    "id": "integer (task ID)",
    "user_id": "string (user ID)",
    "title": "string (task title)",
    "description": "string (task description)",
    "completed": "boolean (completion status)",
    "priority": "string (high/medium/low)",
    "tags": ["string (tag names)"],
    "due_date": "string (ISO 8601 date, optional)",
    "is_recurring": "boolean (recurring flag)",
    "recurring_interval": "string (daily/weekly, optional)",
    "created_at": "string (ISO 8601 datetime)"
  }
  ```
- **Errors**: 400 (Bad request), 401 (Unauthorized), 403 (Forbidden), 422 (Validation error)

### GET /api/{user_id}/tasks/{id}
- **Purpose**: Retrieve a specific task
- **Headers**: Authorization: Bearer {token}
- **Response (200)**:
  ```json
  {
    "id": "integer (task ID)",
    "user_id": "string (user ID)",
    "title": "string (task title)",
    "description": "string (task description)",
    "completed": "boolean (completion status)",
    "priority": "string (high/medium/low)",
    "tags": ["string (tag names)"],
    "due_date": "string (ISO 8601 date, optional)",
    "is_recurring": "boolean (recurring flag)",
    "recurring_interval": "string (daily/weekly, optional)",
    "created_at": "string (ISO 8601 datetime)"
  }
  ```
- **Errors**: 401 (Unauthorized), 403 (Forbidden - wrong user ID or not user's task), 404 (Not found)

### PUT /api/{user_id}/tasks/{id}
- **Purpose**: Update an existing task
- **Headers**: Authorization: Bearer {token}
- **Request**: Same as POST but all fields optional
- **Response (200)**:
  ```json
  {
    "id": "integer (task ID)",
    "user_id": "string (user ID)",
    "title": "string (task title)",
    "description": "string (task description)",
    "completed": "boolean (completion status)",
    "priority": "string (high/medium/low)",
    "tags": ["string (tag names)"],
    "due_date": "string (ISO 8601 date, optional)",
    "is_recurring": "boolean (recurring flag)",
    "recurring_interval": "string (daily/weekly, optional)",
    "created_at": "string (ISO 8601 datetime)"
  }
  ```
- **Errors**: 400 (Bad request), 401 (Unauthorized), 403 (Forbidden), 404 (Not found), 422 (Validation error)

### DELETE /api/{user_id}/tasks/{id}
- **Purpose**: Delete a task
- **Headers**: Authorization: Bearer {token}
- **Response (204)**: No content
- **Errors**: 401 (Unauthorized), 403 (Forbidden), 404 (Not found)

## Error Response Format
```json
{
  "detail": "error message"
}
```

## Common Error Codes
- 400: Bad Request - Invalid request format or data
- 401: Unauthorized - Missing or invalid authentication token
- 403: Forbidden - User doesn't have permission for this resource
- 404: Not Found - Requested resource doesn't exist
- 422: Unprocessable Entity - Validation error in request data
- 500: Internal Server Error - Server-side error