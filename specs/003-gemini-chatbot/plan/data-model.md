# Data Model: Phase III - Gemini-Powered Chatbot

**Feature**: Gemini-Powered Chatbot
**Created**: 2026-02-01
**Status**: Complete

## Entities

### Conversation
**Purpose**: Stores chat conversation sessions between users and AI assistant

**Fields**:
- `id` (UUID/String): Unique identifier for the conversation
- `user_id` (String): Reference to the user who owns this conversation
- `title` (String): Auto-generated title based on first message or user's intent
- `created_at` (DateTime): Timestamp when conversation started
- `updated_at` (DateTime): Last activity timestamp
- `is_active` (Boolean): Whether conversation is currently active

**Relationships**:
- One-to-many with `Message` entity (one conversation has many messages)
- Many-to-one with `User` entity (many conversations belong to one user)

**Validation**:
- `user_id` must exist in users table
- `title` must be between 1-100 characters
- `created_at` and `updated_at` are auto-generated timestamps

### Message
**Purpose**: Stores individual messages within a conversation

**Fields**:
- `id` (Integer): Unique identifier for the message
- `conversation_id` (String): Reference to parent conversation
- `role` (String): Either "user" or "assistant"
- `content` (String): The actual message content
- `timestamp` (DateTime): When the message was created
- `metadata` (JSON): Additional information (e.g., tool calls, task references)

**Relationships**:
- Many-to-one with `Conversation` entity (many messages belong to one conversation)

**Validation**:
- `conversation_id` must exist in conversations table
- `role` must be either "user" or "assistant"
- `content` must not exceed 10,000 characters
- `timestamp` is auto-generated

### Task (Extended)
**Purpose**: Existing task entity with potential AI interaction metadata

**Additional Fields (if needed)**:
- `ai_generated` (Boolean): Whether task was created via AI interaction
- `conversation_reference` (String): Link to conversation that created this task
- `ai_priority_score` (Float): AI-determined priority score (0.0-1.0)

**Relationships**:
- Many-to-one with `User` entity (many tasks belong to one user)
- Optional relationship with `Conversation` via `conversation_reference`

## State Transitions

### Conversation
- **Active**: New conversation or recent activity
- **Inactive**: No activity for extended period
- **Archived**: User-requested archival or system cleanup

### Message
- **Pending**: Message sent but awaiting AI response
- **Processing**: AI is generating response
- **Completed**: Response generated and delivered
- **Error**: Error occurred during processing

## Indexes

### Conversation Table
- Index on `user_id` for efficient user conversation retrieval
- Index on `updated_at` for chronological ordering
- Composite index on `(user_id, updated_at)` for user timeline queries

### Message Table
- Index on `conversation_id` for conversation message retrieval
- Index on `timestamp` for chronological ordering
- Composite index on `(conversation_id, timestamp)` for conversation timeline queries

## Constraints

### Conversation
- Foreign key constraint: `user_id` references `users.id`
- Unique constraint: Prevent duplicate conversations for same user within short timeframe

### Message
- Foreign key constraint: `conversation_id` references `conversations.id`
- Check constraint: `role` must be in ["user", "assistant"]

## API Integration Points

### Conversation Management
- Create new conversation when user starts chat
- Update conversation title and timestamps on activity
- Archive old conversations to optimize performance

### Message Management
- Add user message when chat input received
- Add AI response message after processing
- Retrieve message history for conversation continuation