# Speckitplus-Hackathon-II - Phase II Todo Application

## Overview

This is a full-stack web application for task management built as part of the Speckitplus Hackathon. The application features a Next.js frontend with a FastAPI backend, providing a modern task management experience with advanced organization features.

## Features

- **Task Management**: Create, read, update, and delete tasks
- **Advanced Organization**:
  - Priority levels (High, Medium, Low)
  - Tags/Categories for tasks
  - Search and filter functionality
  - Sorting by due date, priority, or title
- **Authentication**: Secure user authentication with JWT tokens
- **Responsive Design**: Works on desktop and mobile devices
- **Modern UI**: Clean, intuitive interface with shadcn-like design

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL (with SQLModel ORM)
- **Authentication**: JWT-based authentication
- **Dependencies**:
  - fastapi==0.128.0
  - sqlmodel==0.0.31
  - uvicorn==0.40.0
  - python-jose[cryptography]==3.5.0
  - passlib[bcrypt]==1.7.4
  - alembic==1.17.2

### Frontend
- **Framework**: Next.js 16+ with App Router
- **Styling**: Tailwind CSS with shadcn-inspired components
- **State Management**: React Context API for authentication
- **Dependencies**:
  - next==16.0.0
  - react==19.0.0
  - react-dom==19.0.0
  - tailwindcss==3.4.0
  - better-auth==0.1.0

## Project Structure

```
Speckitplus-Hackathon-II/
├── backend/
│   ├── api/          # API route handlers
│   ├── core/         # Core utilities (database, security)
│   ├── models/       # Database models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   ├── alembic/      # Database migrations
│   └── main.py       # Main application entry point
├── frontend/
│   ├── app/          # Next.js App Router pages
│   ├── components/   # React components
│   ├── lib/          # Utilities and API clients
│   └── public/       # Static assets
├── specs/            # Project specifications
└── .env.example      # Environment variables template
```

## Setup Instructions

### Backend Setup

1. **Install Python dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp ../.env.example .env
   # Edit .env with your configuration
   ```

3. **Run the backend server**:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

### Frontend Setup

1. **Install Node.js dependencies**:
   ```bash
   cd frontend
   npm install
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env.local
   # Edit .env.local with your configuration
   ```

3. **Run the development server**:
   ```bash
   cd frontend
   npm run dev
   ```

## API Endpoints

### Authentication
- `POST /api/register` - User registration
- `POST /api/login` - User login
- `GET /api/me` - Get current user info

### Tasks
- `GET /api/users/{user_id}/tasks` - Get tasks for a user (with filtering/sorting)
- `POST /api/users/{user_id}/tasks` - Create a new task
- `GET /api/users/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/users/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/users/{user_id}/tasks/{task_id}` - Delete a task

## Environment Variables

### Backend (.env)
- `DATABASE_URL` - Database connection string
- `JWT_SECRET_KEY` - Secret key for JWT tokens
- `JWT_ALGORITHM` - JWT algorithm (default: HS256)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration time

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL` - Backend API URL

## Running the Application

1. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

2. In a new terminal, start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Open your browser to `http://localhost:3000`

## Database Migrations

The project uses Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Migration message"

# Apply migrations
alembic upgrade head
```

## Development Notes

- The frontend uses a custom UI component library inspired by shadcn/ui
- Authentication is implemented with JWT tokens stored in localStorage
- The application follows a monorepo structure with clear separation between frontend and backend
- All API calls are made through the `apiClient` utility in `frontend/lib/api.ts`
- The backend enforces user data isolation - users can only access their own tasks

## Future Enhancements (Phase V)

- Kafka integration for recurring tasks
- Email and browser push notifications
- Advanced analytics and reporting
- Team/collaboration features