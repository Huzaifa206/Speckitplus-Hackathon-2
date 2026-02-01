# Quickstart Guide: Phase III - Gemini-Powered Chatbot

## Prerequisites

- Python 3.9+ installed
- Node.js 18+ installed
- Access to Google Gemini API
- Existing Phase II codebase (frontend and backend)

## Setup Instructions

### 1. Clone Phase II Code
```bash
# Create Phase 3 directory structure
mkdir -p phase-3/{frontend,backend}

# Copy Phase II frontend to Phase 3
cp -r frontend/* phase-3/frontend/

# Copy Phase II backend to Phase 3
cp -r backend/* phase-3/backend/
```

### 2. Backend Configuration

#### Install Dependencies
```bash
cd phase-3/backend
pip install openai python-dotenv
```

#### Configure Environment
Create `.env` file in `phase-3/backend/`:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
DATABASE_URL=postgresql://your_neon_db_url
```

### 3. Frontend Configuration

#### Install Dependencies
```bash
cd phase-3/frontend
npm install openai
```

### 4. Database Extensions

Add conversation and message tables to existing database schema in `phase-3/backend/models/`:
- `Conversation` model
- `Message` model

### 5. Run the Application

#### Backend
```bash
cd phase-3/backend
uvicorn main:app --reload
```

#### Frontend
```bash
cd phase-3/frontend
npm run dev
```

## Key Components

### MCP Tools (`phase-3/backend/mcp_tools.py`)
- `add_task()`: Create new tasks
- `list_tasks()`: Retrieve user tasks
- `complete_task()`: Mark tasks as completed
- `delete_task()`: Remove tasks

### Agent Logic (`phase-3/backend/agent.py`)
- Google Gemini integration via OpenAI SDK
- Tool execution framework
- Conversation management

### Chat API (`phase-3/backend/api/chat.py`)
- `/api/chat`: Main chat endpoint
- `/api/conversations`: Conversation listing
- `/api/conversations/{id}/messages`: Message history

### Chat Interface (`phase-3/frontend/app/chat-widget.tsx`)
- Floating chat widget
- Conversation history display
- Real-time messaging

## Testing

### Verify Isolation
- Ensure Phase II code in root directories remains unchanged
- Verify Phase 3 runs independently

### Test AI Integration
- Start a conversation with the chatbot
- Verify natural language task creation works
- Check that MCP tools execute properly

### Validate Security
- Confirm API keys are loaded from environment
- Verify authentication still works
- Check that inputs are properly sanitized

## Troubleshooting

### Gemini API Issues
- Verify `GEMINI_API_KEY` is correctly set
- Check Google API quota limits
- Confirm base URL is set to `https://generativelanguage.googleapis.com/v1beta/openai/`

### Database Issues
- Ensure new conversation/message tables are created
- Verify existing task data is accessible
- Check foreign key relationships

### Frontend Issues
- Confirm chat widget loads properly
- Verify WebSocket connections (if used)
- Check CORS settings for cross-origin requests