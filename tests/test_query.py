"""
Unit tests for search, filter, and sort functionality.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.core.models import Task
from src.features.query import filter_tasks, search_tasks, sort_tasks, execute_query_pipeline


def test_filtering():
    """Test filtering functionality."""
    # Create sample tasks
    task1 = Task(id=1, title="Work Task", description="Task for work", priority="high", tags=["work", "urgent"])
    task2 = Task(id=2, title="Personal Task", description="Personal task", priority="medium", tags=["personal"])
    task3 = Task(id=3, title="Completed Task", description="Already done", priority="low", tags=["completed"], completed=True)
    
    tasks = [task1, task2, task3]
    
    # Test status filtering
    pending_tasks = filter_tasks(tasks, status="pending")
    assert len(pending_tasks) == 2  # task1 and task2 are pending
    
    completed_tasks = filter_tasks(tasks, status="completed")
    assert len(completed_tasks) == 1  # task3 is completed
    assert completed_tasks[0].id == 3
    
    # Test priority filtering
    high_priority_tasks = filter_tasks(tasks, priority="high")
    assert len(high_priority_tasks) == 1
    assert high_priority_tasks[0].id == 1
    
    # Test tag filtering (OR logic)
    work_urgent_tasks = filter_tasks(tasks, tags=["work", "completed"])
    assert len(work_urgent_tasks) == 2  # task1 has "work", task3 has "completed"
    
    # Test combined filtering
    pending_high_tasks = filter_tasks(tasks, status="pending", priority="high")
    assert len(pending_high_tasks) == 1
    assert pending_high_tasks[0].id == 1
    
    print("✓ Filtering tests passed")


def test_searching():
    """Test searching functionality."""
    # Create sample tasks
    task1 = Task(id=1, title="Meeting Preparation", description="Prepare for team meeting")
    task2 = Task(id=2, title="Grocery Shopping", description="Buy groceries for dinner")
    task3 = Task(id=3, title="Code Review", description="Review teammate's code")
    
    tasks = [task1, task2, task3]
    
    # Test search in title
    meeting_results = search_tasks(tasks, "meeting")
    assert len(meeting_results) == 1
    assert meeting_results[0].id == 1
    
    # Test search in description
    code_results = search_tasks(tasks, "code")
    assert len(code_results) == 1
    assert code_results[0].id == 3
    
    # Test case-insensitive search
    MEETING_results = search_tasks(tasks, "MEETING")
    assert len(MEETING_results) == 1
    assert MEETING_results[0].id == 1
    
    # Test no results
    no_results = search_tasks(tasks, "nonexistent")
    assert len(no_results) == 0
    
    print("✓ Searching tests passed")


def test_sorting():
    """Test sorting functionality."""
    # Create sample tasks
    task1 = Task(id=1, title="Low Priority Task", priority="low")
    task2 = Task(id=2, title="High Priority Task", priority="high")
    task3 = Task(id=3, title="Medium Priority Task", priority="medium")
    
    tasks = [task1, task2, task3]
    
    # Test priority sorting
    sorted_by_priority = sort_tasks(tasks, "priority")
    assert sorted_by_priority[0].priority == "high"  # High priority first
    assert sorted_by_priority[1].priority == "medium"  # Medium priority second
    assert sorted_by_priority[2].priority == "low"  # Low priority last
    
    # Test title sorting
    sorted_by_title = sort_tasks(tasks, "title")
    titles = [task.title for task in sorted_by_title]
    assert "High Priority Task" in titles[0]  # Alphabetically first
    assert "Low Priority Task" in titles[1]  # Alphabetically middle
    assert "Medium Priority Task" in titles[2]  # Alphabetically last
    
    print("✓ Sorting tests passed")


def test_query_pipeline():
    """Test the full query pipeline."""
    # Create sample tasks
    task1 = Task(id=1, title="Meeting Preparation", description="Prepare for team meeting", priority="high", tags=["work", "urgent"])
    task2 = Task(id=2, title="Grocery Shopping", description="Buy groceries for dinner", priority="medium", tags=["personal"])
    task3 = Task(id=3, title="Code Review", description="Review teammate's code", priority="low", tags=["work"], completed=True)
    
    tasks = [task1, task2, task3]
    
    # Test pipeline with search and filter
    results = execute_query_pipeline(tasks, keyword="meeting", priority="high")
    assert len(results) == 1
    assert results[0].id == 1
    
    # Test pipeline with tag filter
    work_results = execute_query_pipeline(tasks, tags=["work"])
    assert len(work_results) == 2  # task1 and task3 have "work" tag
    
    # Test pipeline with status filter
    completed_results = execute_query_pipeline(tasks, status="completed")
    assert len(completed_results) == 1
    assert completed_results[0].id == 3
    
    print("✓ Query pipeline tests passed")


if __name__ == "__main__":
    test_filtering()
    test_searching()
    test_sorting()
    test_query_pipeline()
    print("\nAll search, filter, and sort functionality tests passed!")