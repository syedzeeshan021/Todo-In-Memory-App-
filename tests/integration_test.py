"""
Basic integration test to verify the todo application functionality.
"""
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.models import Task
from src.core.crud import TaskManager
from src.features.priorities_tags import normalize_priority, parse_tags_from_string
from src.features.query import execute_query_pipeline


def test_basic_functionality():
    """Test basic functionality of the todo application."""
    print("Testing basic functionality...")
    
    # Test Task creation
    task = Task(id=1, title="Test Task", description="Test Description")
    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.priority == "medium"  # Default priority
    print("PASS: Task creation works")
    
    # Test TaskManager
    tm = TaskManager()
    tm.create_task("First Task", "Description of first task")
    tm.create_task("Second Task", "Description of second task", priority="high")
    tm.create_task("Third Task", "Description of third task", tags=["work", "urgent"])
    
    assert len(tm.tasks) == 3
    print("✓ TaskManager CRUD operations work")
    
    # Test priority normalization
    assert normalize_priority("HIGH") == "high"
    assert normalize_priority("Medium") == "medium"
    assert normalize_priority("low") == "low"
    print("✓ Priority normalization works")
    
    # Test tag parsing
    tags = parse_tags_from_string("work, urgent, home")
    assert "work" in tags
    assert "urgent" in tags
    assert "home" in tags
    print("✓ Tag parsing works")
    
    # Test query pipeline
    all_tasks = list(tm.tasks.values())
    high_priority_tasks = execute_query_pipeline(all_tasks, priority="high")
    assert len(high_priority_tasks) == 1
    print("✓ Query pipeline works")
    
    # Test filtering by tags
    tagged_tasks = execute_query_pipeline(all_tasks, tags=["work"])
    assert len(tagged_tasks) >= 1  # At least the third task should match
    print("✓ Tag filtering works")
    
    print("\nAll basic functionality tests passed! ✓")


if __name__ == "__main__":
    test_basic_functionality()