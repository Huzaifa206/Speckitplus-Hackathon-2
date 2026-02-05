"""
Migrate tasks from 'default_user' to a real user account
"""
from sqlmodel import Session, select
from core.database import get_db_session
from models.task import Task

def migrate_tasks(from_user_id: str, to_user_id: str):
    """
    Migrate all tasks from one user to another
    """
    print(f"Migrating tasks from '{from_user_id}' to '{to_user_id}'...")

    with get_db_session() as session:
        # Get all tasks for the source user
        statement = select(Task).where(Task.user_id == from_user_id)
        tasks = session.exec(statement).all()

        if not tasks:
            print(f"No tasks found for user '{from_user_id}'")
            return

        print(f"Found {len(tasks)} tasks to migrate:")
        for task in tasks:
            print(f"  - Task #{task.id}: {task.title}")

        # Ask for confirmation
        confirm = input(f"\nMigrate these {len(tasks)} tasks to user '{to_user_id}'? (yes/no): ")

        if confirm.lower() != 'yes':
            print("Migration cancelled")
            return

        # Update all tasks
        migrated_count = 0
        for task in tasks:
            task.user_id = to_user_id
            session.add(task)
            migrated_count += 1

        session.commit()
        print(f"\n✓ Successfully migrated {migrated_count} tasks!")

if __name__ == "__main__":
    print("=" * 60)
    print("TASK MIGRATION TOOL")
    print("=" * 60)

    # Show current user distribution
    with get_db_session() as session:
        statement = select(Task)
        all_tasks = session.exec(statement).all()

        users = {}
        for task in all_tasks:
            if task.user_id not in users:
                users[task.user_id] = []
            users[task.user_id].append(task)

        print("\nCurrent task distribution:")
        for i, (user_id, user_tasks) in enumerate(users.items(), 1):
            print(f"  {i}. {user_id}: {len(user_tasks)} tasks")

    print("\n" + "=" * 60)

    # Get migration parameters
    from_user = input("Enter source user_id (e.g., 'default_user'): ").strip()
    to_user = input("Enter destination user_id: ").strip()

    if not from_user or not to_user:
        print("Error: Both user IDs are required")
        exit(1)

    if from_user == to_user:
        print("Error: Source and destination users cannot be the same")
        exit(1)

    migrate_tasks(from_user, to_user)
    print("=" * 60)
