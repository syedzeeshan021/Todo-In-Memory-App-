"""
Integration tests to verify backward compatibility and feature interaction.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.core.models import Task
from src.core.crud import TaskManager
from src.features.priorities_tags import normalize_priority, parse_tags_from_string
from src.features.query import execute_query_pipeline


def test_backward_compatibility():
    """Test that basic functionality still works as expected."""
    # Create a TaskManager
    tm = TaskManager()
    
    # Test basic task creation (without priority/tags)
    task = tm.create_task("Basic Task", "Description of basic task")
    assert task.title == "Basic Task"
    assert task.description == "Description of basic task"
    assert task.priority == "medium"  # Default priority
    assert task.tags == []  # Default tags
    
    # Test that we can still create tasks with just title and description
    task2 = tm.create_task("Another Task", "Another description")
    assert task2.title == "Another Task"
    assert task2.priority == "medium"  # Still default priority
    assert task2.tags == []  # Still default tags
    
    # Test basic listing
    all_tasks = tm.list_tasks()
    assert len(all_tasks) == 2
    
    # Test that basic update still works
    updated_task = tm.update_task(task.id, "Updated Title", "Updated Description")
    assert updated_task.title == "Updated Title"
    
    print("✓ Backward compatibility tests passed")


def test_feature_interaction():
    """Test that different features work together."""
    tm = TaskManager()
    
    # Create tasks with various combinations of features
    task1 = tm.create_task("High Priority Work Task", "Description", priority="high", tags=["work", "urgent"])
    task2 = tm.create_task("Low Priority Personal Task", "Description", priority="low", tags=["personal"])
    task3 = tm.create_task("Medium Priority Meeting", "Meeting notes", priority="medium", tags=["work", "meeting"])
    
    # Mark one task as completed
    tm.toggle_completion(task2.id)
    
    # Test combined filtering: work tasks that are pending
    work_pending = tm.list_tasks(status="pending", tags=["work"])
    assert len(work_pending) == 2  # task1 and task3 are work tasks and pending
    
    # Test combined filtering: high priority tasks with 'urgent' tag
    high_urgent = tm.list_tasks(priority="high", tags=["urgent"])
    assert len(high_urgent) == 1
    assert high_urgent[0].id == task1.id
    
    # Test search within filtered results
    search_results = tm.search_tasks("meeting", tags=["work"])
    assert len(search_results) == 1
    assert search_results[0].id == task3.id
    
    # Test sorting within filtered results
    sorted_work_tasks = tm.list_tasks(tags=["work"], sort_by="priority")
    # Should be ordered: high (task1), medium (task3), low (not included since it's not tagged work)
    assert sorted_work_tasks[0].priority == "high"
    assert sorted_work_tasks[1].priority == "medium"
    
    print("✓ Feature interaction tests passed")


def test_edge_cases():
    """Test edge cases and error conditions."""
    tm = TaskManager()
    
    # Test empty tag string handling
    task_with_empty_tags = tm.create_task("Task with empty tags", "Description", tags=["", "valid", "  "])
    # Empty tags should be filtered out
    assert "valid" in task_with_empty_tags.tags
    assert len(task_with_empty_tags.tags) == 1  # Only "valid" should remain
    
    # Test case-insensitive priority handling
    task_upper_priority = tm.create_task("Upper case priority", "Description", priority="HIGH")
    assert task_upper_priority.priority == "high"  # Should be normalized
    
    # Test tag parsing with extra whitespace
    parsed_tags = parse_tags_from_string("  work  ,  personal  ,  urgent  ")
    assert "work" in parsed_tags
    assert "personal" in parsed_tags
    assert "urgent" in parsed_tags
    assert len(parsed_tags) == 3
    
    print("✓ Edge case tests passed")


if __name__ == "__main__":
    test_backward_compatibility()
    test_feature_interaction()
    test_edge_cases()
    print("\nAll integration tests passed!")