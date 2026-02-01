# Phase 3 - Gemini-Powered Chatbot

This directory contains the implementation of the Gemini-powered chatbot feature for the task management application.

## Overview

Phase 3 introduces a natural language AI assistant that can help users manage their tasks through conversational interactions. The system uses Google's Gemini model via the OpenAI compatibility layer to understand user requests and execute appropriate task operations.

## Architecture

- **Frontend**: Next.js application with a chat widget integrated into the dashboard
- **Backend**: FastAPI application with Gemini integration and MCP tools
- **Database**: PostgreSQL (Neon) with additional Conversation and Message tables
- **AI Integration**: Google Gemini via OpenAI compatibility layer

## Features

- Natural language task management (add, list, complete, delete tasks)
- Conversation history with persistent storage
- Tool-based execution for database operations
- Rate limiting and input sanitization
- Error handling and graceful degradation

## Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- Google Gemini API key
- PostgreSQL database (or use the existing SQLite for development)

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd phase-3/backend
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your configuration:
   ```env
   GEMINI_API_KEY=your_google_gemini_api_key_here
   DATABASE_URL=postgresql://your_neon_db_url
   ```

5. Run the application:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd phase-3/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

## API Endpoints

- `POST /api/chat` - Process user input and return AI response
- `GET /api/chat/conversations` - List user conversations
- `GET /api/chat/conversations/{id}/messages` - Get messages for a conversation

## Security

- Input sanitization to prevent injection attacks
- Rate limiting to prevent abuse
- Environment variable validation
- Proper authentication (inherits from Phase 2)

## Isolation

Phase 3 is completely isolated from Phase 2 code:
- All code resides in the `/phase-3` directory
- Separate frontend and backend applications
- Independent dependencies and configurations
- No modifications to the original `/frontend` and `/backend` directories