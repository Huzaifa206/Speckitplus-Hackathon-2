"""
Basic test to verify the application structure and imports
"""

def test_backend_imports():
    """Test that all backend modules can be imported without errors"""
    try:
        # Test core modules
        from backend.core.database import get_session, create_db_and_tables
        from backend.core.security import create_access_token, verify_token

        # Test models
        from backend.models.user import User, UserBase
        from backend.models.task import Task, TaskBase, PriorityEnum

        # Test services
        from backend.services.user_service import get_user_by_email, create_user
        from backend.services.task_service import get_tasks_by_user, create_task

        # Test API routes
        from backend.api.auth import router as auth_router
        from backend.api.tasks import router as tasks_router

        # Test main app
        from backend.main import app

        print("✅ All backend modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_frontend_structure():
    """Test that key frontend files exist"""
    import os

    frontend_files = [
        "frontend/app/layout.tsx",
        "frontend/app/page.tsx",
        "frontend/components/ui/button.tsx",
        "frontend/components/task/task-dashboard.tsx",
        "frontend/lib/types.ts",
        "frontend/lib/api.ts"
    ]

    all_exist = True
    for file in frontend_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
            all_exist = False

    return all_exist

if __name__ == "__main__":
    print("Testing application structure...\n")

    print("Testing backend imports:")
    backend_ok = test_backend_imports()

    print("\nTesting frontend structure:")
    frontend_ok = test_frontend_structure()

    print(f"\nOverall result:")
    if backend_ok and frontend_ok:
        print("✅ Application structure is complete!")
    else:
        print("❌ Some issues were found in the application structure.")