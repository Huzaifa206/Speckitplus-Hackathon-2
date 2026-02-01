# Implementation Plan: Phase III - Gemini-Powered Chatbot

**Feature**: Gemini-Powered Chatbot
**Branch**: 003-gemini-chatbot
**Created**: 2026-02-01
**Status**: Draft

## Technical Context

### Architecture Overview
- **Project Structure**: `/phase-3` directory containing separate frontend and backend
- **Agent Logic**: FastAPI backend with OpenAI-compatible Gemini client
- **Database**: Existing Neon DB with new Conversation/Message tables
- **Frontend**: Next.js with chat interface widget

### Known Elements
- Phase II frontend (Next.js) and backend (FastAPI) exist and functional
- SQLModel ORM with Neon PostgreSQL database in place
- Existing task management functionality
- Authentication system already implemented

### Unknown Elements
- **NEEDS CLARIFICATION**: Specific Gemini model selection (gemini-1.5-flash vs gemini-2.0-flash)
- **NEEDS CLARIFICATION**: Conversation history storage mechanism (in DB vs session)
- **NEEDS CLARIFICATION**: Chat UI integration approach (widget overlay vs dedicated page)

## Constitution Check

### Compliance Verification
- ✅ **Isolation Principle**: Code will reside in dedicated `/phase-3` directory
- ✅ **Stateless Agent**: AI service will be stateless with DB-stored conversation history
- ✅ **Model Provider**: Using Google Gemini via OpenAI Compatibility layer
- ✅ **Tool-Driven Architecture**: AI will use MCP tools instead of direct DB access
- ✅ **Security**: Secrets via `.env` (`GEMINI_API_KEY`) and input sanitization

### Gates
- **Gate 1**: Phase II functionality must remain untouched in root directories
- **Gate 2**: MCP tools must be implemented before AI integration
- **Gate 3**: Gemini API integration must be properly configured with error handling

## Phase 0: Outline & Research

### Research Tasks
1. **Gemini Model Selection**: Compare gemini-1.5-flash vs gemini-2.0-flash for task management
2. **OpenAI SDK Integration**: Research Google Gemini integration via OpenAI-compatible endpoint
3. **Conversation Storage**: Best practices for storing chat history in PostgreSQL
4. **Chat UI Patterns**: Recommended approaches for chat widgets in Next.js applications
5. **MCP Tool Implementation**: Best practices for implementing Model Context Protocol tools

### Expected Outcomes
- Decision on optimal Gemini model for task management
- Understanding of Google's OpenAI compatibility layer
- Conversation storage strategy
- Chat UI implementation approach
- MCP tool patterns for database operations

## Phase 1: Design & Contracts

### Data Model Design
- **Conversation Entity**: Stores conversation sessions with metadata
- **Message Entity**: Stores individual messages with role (user/assistant) and content
- **Task Entity**: Existing entity extended with AI interaction metadata if needed

### API Contract Design
- **POST /api/chat**: Handles user input and returns AI response with tool execution
- **GET /api/conversations**: Lists user conversations
- **GET /api/conversations/{id}/messages**: Retrieves messages for specific conversation

### Agent Context Update
- Update agent context with Gemini integration patterns
- Add MCP tool implementation guidelines
- Include conversation management protocols

## Phase 2: Implementation Steps

### Step 1: Scaffold Phase 3
- Create `/phase-3` directory structure
- Copy Phase II frontend and backend to respective subdirectories
- Verify existing functionality remains intact

### Step 2: Database Extensions
- Add `conversations` and `messages` tables to existing schema
- Implement data models for conversation history
- Ensure proper indexing for performance

### Step 3: MCP Tool Implementation
- Create `phase-3/backend/mcp_tools.py`
- Implement `add_task`, `list_tasks`, `complete_task`, `delete_task` functions
- Ensure tools access DB on behalf of user with proper authentication

### Step 4: Agent Logic
- Create `phase-3/backend/agent.py`
- Implement OpenAI client with Google Gemini configuration
- Build chat processing pipeline: Load History → Append User Msg → Call Gemini → Execute Tools → Save Response

### Step 5: API Endpoint
- Create `POST /api/chat` endpoint
- Implement conversation management logic
- Add error handling and rate limiting

### Step 6: Frontend Integration
- Add chat widget to dashboard
- Implement conversation history display
- Connect to backend API endpoint

### Step 7: Configuration
- Update `/phase-3/backend/.env` with `GEMINI_API_KEY`
- Install required dependencies (`openai` package)
- Configure CORS for chat interface

### Step 8: Testing
- Unit tests for MCP tools
- Integration tests for agent logic
- End-to-end tests for chat functionality
- Verify isolation from Phase II code

## Success Criteria Verification
- Natural language task creation succeeds in 90% of attempts
- Chat response time under 5 seconds for 95% of interactions
- Zero regression in Phase II functionality
- All MCP tools execute intended operations correctly
- Conversation history maintained properly during sessions