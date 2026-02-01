# Research: Phase III - Gemini-Powered Chatbot

**Feature**: Gemini-Powered Chatbot
**Created**: 2026-02-01
**Status**: Complete

## Research Findings

### 1. Gemini Model Selection

**Decision**: Use `gemini-1.5-flash` model
**Rationale**: The gemini-1.5-flash model offers optimal balance of speed, cost, and capabilities for task management conversations. It has strong reasoning abilities while maintaining fast response times, making it ideal for real-time chat interactions.
**Alternatives considered**:
- gemini-2.0-flash: Still in development, not generally available
- gemini-1.5-pro: Higher cost and slower response times for this use case
- gemini-1.0-pro: Less capable reasoning for complex task management scenarios

### 2. OpenAI SDK Integration

**Decision**: Use OpenAI Python SDK with Google's OpenAI-compatible endpoint
**Rationale**: Google's OpenAI-compatible endpoint allows using the familiar OpenAI SDK while connecting to Gemini models, reducing development complexity and leveraging existing community knowledge.
**Configuration**:
```python
client = OpenAI(
    api_key=os.environ.get("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
```

### 3. Conversation Storage Strategy

**Decision**: Store conversation history in PostgreSQL using dedicated tables
**Rationale**: Storing conversations in the same database as tasks ensures consistency and allows for complex queries linking tasks and conversations. This approach maintains the stateless nature of the AI service while persisting important conversation context.
**Implementation**: Create `conversations` and `messages` tables with proper relationships and indexing.

### 4. Chat UI Implementation

**Decision**: Integrate chat widget as a floating panel on the dashboard
**Rationale**: A floating chat widget provides easy access without disrupting the main task management interface. This pattern is common in productivity applications and allows users to interact naturally while viewing their tasks.
**Approach**: Implement using Next.js with React components that overlay on top of the dashboard.

### 5. MCP Tool Implementation Patterns

**Decision**: Create synchronous Python functions that map to existing backend operations
**Rationale**: MCP tools should mirror the existing API functionality but be callable from the AI agent. This ensures consistency and leverages existing authentication and business logic.
**Pattern**: Functions that accept parameters from the AI and delegate to existing service layer methods.

## Implementation Guidelines

### Conversation Data Model
- `Conversation`: id, user_id, created_at, updated_at, title (derived from first message)
- `Message`: id, conversation_id, role (user/assistant), content, timestamp, metadata

### Error Handling
- Implement graceful degradation when Gemini API is unavailable
- Provide informative error messages to users
- Log API failures for monitoring

### Security Considerations
- Sanitize all inputs from AI responses before displaying
- Validate tool parameters before executing database operations
- Ensure proper authentication for all operations

## Technology Stack Confirmation
- **Backend**: FastAPI with existing SQLModel ORM
- **Frontend**: Next.js with React for chat interface
- **AI Integration**: OpenAI SDK with Google Gemini endpoint
- **Database**: PostgreSQL (Neon) with new conversation tables
- **Authentication**: Leverage existing authentication system