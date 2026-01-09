# Quickstart: Full-Stack Web Application

## Prerequisites
- Node.js 18+ for frontend
- Python 3.13+ for backend
- pnpm package manager (recommended) or npm/yarn
- UV package manager for Python
- Neon PostgreSQL account

## Setup

### 1. Environment Configuration
1. Create a `.env` file in the root directory based on `.env.example`
2. Configure the following environment variables:
   - `DATABASE_URL`: Neon PostgreSQL connection string
   - `AUTH_SECRET`: Secret key for JWT tokens
   - `NEXT_PUBLIC_AUTH_URL`: Frontend authentication URL

### 2. Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install Python dependencies: `uv sync` or `pip install -r requirements.txt`
3. Set up the database: `alembic upgrade head`
4. Start the backend server: `uv run python main.py` or `python main.py`

### 3. Frontend Setup
1. Navigate to the root directory: `cd ..` (if in backend)
2. Install frontend dependencies: `pnpm install` (or npm install/yarn install)
3. Start the frontend development server: `pnpm dev` (or npm run dev/yarn dev)

## Usage

### Development Mode
- Frontend: Available at `http://localhost:3000`
- Backend API: Available at `http://localhost:8000`
- Backend API Documentation: Available at `http://localhost:8000/docs`

### Authentication
1. Users must register/login through the frontend UI
2. JWT tokens are automatically handled by Better Auth
3. Backend verifies JWT tokens on all protected endpoints

### Core Features
1. **Task Management**: Create, read, update, delete tasks
2. **Organization**: Set priorities (High/Medium/Low) and add custom tags
3. **Search & Filter**: Find tasks by keyword, priority
4. **Sorting**: Sort tasks by due date, priority, or title
5. **Due Dates**: Set due dates for tasks
6. **Recurring Tasks**: Define recurring rules (for future processing)

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout

### Tasks
- `GET /api/{user_id}/tasks` - Get user's tasks with filtering/sorting
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update a task
- `DELETE /api/{user_id}/tasks/{id}` - Delete a task

## Environment Variables

### Backend (.env in backend directory)
- `DATABASE_URL`: Neon PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT token signing
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time

### Frontend (.env in root directory)
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_AUTH_URL`: Authentication service URL
- `AUTH_SECRET`: Secret key for auth (same as backend)

## Development Commands

### Backend
- Run tests: `uv run pytest`
- Run with auto-reload: `uv run uvicorn main:app --reload`
- Run database migrations: `alembic upgrade head`

### Frontend
- Run development server: `pnpm dev`
- Run tests: `pnpm test`
- Build for production: `pnpm build`
- Run linting: `pnpm lint`
- Run type checking: `pnpm type-check`

## Database Migrations
1. After making model changes, create a migration: `alembic revision --autogenerate -m "description"`
2. Apply the migration: `alembic upgrade head`