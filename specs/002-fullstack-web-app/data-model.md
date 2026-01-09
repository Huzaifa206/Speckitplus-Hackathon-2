# Data Model: Full-Stack Web Application

## User Entity

### Fields
- **id** (String): Unique identifier for the user (managed by Better Auth)
- **email** (str): User's email address, unique
- **name** (str): User's display name
- **created_at** (datetime): Account creation timestamp
- **updated_at** (datetime): Last update timestamp

### Validation Rules
- Email must be a valid email format
- Email must be unique across all users
- Name must not be empty

## Task Entity

### Fields
- **id** (Integer): Primary key, unique identifier for the task
- **user_id** (String): Foreign key linking to user (managed by Better Auth)
- **title** (str): Task title, required
- **description** (str): Detailed task description, optional
- **completed** (bool): Completion status, default false
- **priority** (str): Priority level enum (High, Medium, Low), default "Medium"
- **tags** (JSON or Array of Strings): Task tags for organization, optional
- **due_date** (datetime): Due date for the task, optional
- **is_recurring** (bool): Flag indicating if task is recurring, default false
- **recurring_interval** (str): Recurring interval (e.g., "daily", "weekly"), optional
- **created_at** (datetime): Task creation timestamp

### Validation Rules
- Title must not be empty
- Priority must be one of "High", "Medium", "Low"
- Due date must be in the future if provided
- Recurring interval must be one of "daily", "weekly", or null when is_recurring is true
- User ID must reference an existing user
- Tags must be a valid JSON array of strings if provided

### State Transitions
- **Incomplete → Complete**: When mark complete operation is performed
- **Complete → Incomplete**: When mark incomplete operation is performed

## Data Isolation Requirements

### Access Control
- Users can only access their own tasks via user_id foreign key
- No cross-user data access is allowed
- Database-level foreign key constraints enforce relationship integrity
- API endpoints verify user_id matches authenticated user's ID