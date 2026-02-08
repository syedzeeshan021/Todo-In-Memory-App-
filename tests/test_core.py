"""
Basic tests for core CRUD functionality to ensure it works as expected.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.core.models import Task
from src.core.crud import TaskManager


def test_task_creation():
    """Test basic task creation."""
    task = Task(id=1, title="Test Task", description="Test Description")
    
    assert task.id == 1
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed == False
    assert task.priority == "medium"  # Default priority
    assert task.tags == []  # Default tags
    assert task.created_at is not None
    assert task.updated_at is not None
    
    print("✓ Task creation tests passed")


def test_task_updates():
    """Test task update functionality."""
    task = Task(id=1, title="Original Title", description="Original Description")
    
    # Update some fields
    task.update(title="New Title", description="New Description", priority="high")
    
    assert task.title == "New Title"
    assert task.description == "New Description"
    assert task.priority == "high"
    
    # Update only specific fields
    task.update(title="Updated Title")
    assert task.title == "Updated Title"
    assert task.description == "New Description"  # Should remain unchanged
    assert task.priority == "high"  # Should remain unchanged
    
    print("✓ Task update tests passed")


def test_task_validation():
    """Test task validation."""
    # Test title validation
    try:
        Task(id=1, title="", description="Valid description")
        assert False, "Should raise ValueError for empty title"
    except ValueError:
        pass  # Expected
    
    try:
        Task(id=1, title="A" * 201, description="Valid description")  # Too long title
        assert False, "Should raise ValueError for too long title"
    except ValueError:
        pass  # Expected
    
    # Test priority validation
    try:
        Task(id=1, title="Test", description="Test", priority="invalid")
        assert False, "Should raise ValueError for invalid priority"
    except ValueError:
        pass  # Expected
    
    # Test valid priority
    task = Task(id=1, title="Test", description="Test", priority="HIGH")  # Should normalize to lowercase
    assert task.priority == "high"
    
    print("✓ Task validation tests passed")


def test_task_manager_crud():
    """Test TaskManager CRUD operations."""
    tm = TaskManager()
    
    # Test create
    task1 = tm.create_task("Task 1", "Description 1")
    task2 = tm.create_task("Task 2", "Description 2", priority="high", tags=["work"])
    
    assert len(tm.tasks) == 2
    assert task1.id == 1
    assert task2.id == 2
    
    # Test get
    retrieved_task = tm.get_task(1)
    assert retrieved_task is not None
    assert retrieved_task.title == "Task 1"
    
    # Test update
    updated_task = tm.update_task(1, "Updated Task 1", "Updated Description")
    assert updated_task is not None
    assert updated_task.title == "Updated Task 1"
    
    # Test toggle completion
    toggled_task = tm.toggle_completion(1)
    assert toggled_task is not None
    assert toggled_task.completed == True
    
    # Toggle again to make sure it works both ways
    toggled_back_task = tm.toggle_completion(1)
    assert toggled_back_task is not None
    assert toggled_back_task.completed == False
    
    # Test delete
    delete_success = tm.delete_task(2)
    assert delete_success == True
    assert tm.get_task(2) is None
    assert len(tm.tasks) == 1
    
    # Test delete non-existent task
    delete_non_existent = tm.delete_task(999)
    assert delete_non_existent == False
    
    print("✓ TaskManager CRUD tests passed")


if __name__ == "__main__":
    test_task_creation()
    test_task_updates()
    test_task_validation()
    test_task_manager_crud()
    print("\nAll core functionality tests passed!")