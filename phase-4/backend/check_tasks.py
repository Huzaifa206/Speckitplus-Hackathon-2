"""
Quick script to check all tasks in the database
"""
from sqlmodel import Session, select
from core.database import get_db_session
from models.task import Task

print("=" * 60)
print("ALL TASKS IN DATABASE")
print("=" * 60)

with get_db_session() as session:
    statement = select(Task)
    tasks = session.exec(statement).all()

    if not tasks:
        print("No tasks found in database")
    else:
        for task in tasks:
            print(f"\nTask ID: {task.id}")
            print(f"  Title: {task.title}")
            print(f"  User ID: {task.user_id}")
            print(f"  Completed: {task.completed}")
            print(f"  Priority: {task.priority}")
            print(f"  Created: {task.created_at}")
            print("-" * 40)

        print(f"\nTotal tasks: {len(tasks)}")

        # Group by user
        users = {}
        for task in tasks:
            if task.user_id not in users:
                users[task.user_id] = []
            users[task.user_id].append(task)

        print("\nTasks by user:")
        for user_id, user_tasks in users.items():
            print(f"  {user_id}: {len(user_tasks)} tasks")

print("=" * 60)
