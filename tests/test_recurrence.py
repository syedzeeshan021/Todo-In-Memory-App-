"""
Unit tests for recurrence functionality in the todo application.
"""
import pytest
from datetime import datetime, timedelta
from src.core.models import Task
from src.features.recurrence import calculate_next_due, generate_next_occurrence


class TestRecurrence:
    """Test cases for recurrence functionality."""
    
    def test_calculate_next_due_daily(self):
        """Test daily recurrence calculation."""
        original_due = datetime(2026, 2, 15, 9, 0, 0)
        next_due = calculate_next_due(original_due, "daily")
        expected = datetime(2026, 2, 16, 9, 0, 0)
        assert next_due == expected
    
    def test_calculate_next_due_weekly(self):
        """Test weekly recurrence calculation."""
        original_due = datetime(2026, 2, 15, 9, 0, 0)
        next_due = calculate_next_due(original_due, "weekly")
        expected = datetime(2026, 2, 22, 9, 0, 0)
        assert next_due == expected
    
    def test_calculate_next_due_monthly(self):
        """Test monthly recurrence calculation (30-day offset)."""
        original_due = datetime(2026, 2, 15, 9, 0, 0)
        next_due = calculate_next_due(original_due, "monthly")
        expected = datetime(2026, 3, 17, 9, 0, 0)  # Adding 30 days to Feb 15
        assert next_due == expected
    
    def test_calculate_next_due_none(self):
        """Test calculating next due with None original due date."""
        next_due = calculate_next_due(None, "daily")
        assert next_due is None
    
    def test_calculate_next_due_invalid_pattern(self):
        """Test calculating next due with invalid pattern raises ValueError."""
        with pytest.raises(ValueError, match="Invalid recurrence pattern: yearly"):
            calculate_next_due(datetime.now(), "yearly")
    
    def test_generate_next_occurrence_basic(self):
        """Test generating next occurrence with basic properties."""
        from src.core.crud import TaskManager
        
        original_task = Task(
            id=1,
            title="Weekly planning",
            description="Team sync",
            completed=False,
            priority="medium",
            tags=["work"],
            due_date=datetime(2026, 2, 15, 9, 0, 0),
            recurrence="weekly",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Create a mock task manager for testing
        task_manager = TaskManager()
        
        next_task = generate_next_occurrence(original_task, task_manager)
        
        # Verify properties are preserved
        assert next_task.title == original_task.title
        assert next_task.description == original_task.description
        assert next_task.priority == original_task.priority
        assert next_task.tags == original_task.tags
        assert next_task.completed == False  # New occurrence should not be completed
        assert next_task.recurrence == original_task.recurrence
        
        # Verify due date is offset by pattern
        expected_next_due = datetime(2026, 2, 22, 9, 0, 0)  # Weekly offset
        assert next_task.due_date == expected_next_due
    
    def test_generate_next_occurrence_no_due_date(self):
        """Test generating next occurrence when original has no due date."""
        from src.core.crud import TaskManager
        
        original_task = Task(
            id=1,
            title="Daily habit",
            description="Exercise",
            completed=False,
            priority="high",
            tags=[],
            due_date=None,  # No due date
            recurrence="daily",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Create a mock task manager for testing
        task_manager = TaskManager()
        
        next_task = generate_next_occurrence(original_task, task_manager)
        
        # Verify properties are preserved
        assert next_task.title == original_task.title
        assert next_task.description == original_task.description
        assert next_task.priority == original_task.priority
        assert next_task.tags == original_task.tags
        assert next_task.completed == False
        assert next_task.recurrence == original_task.recurrence
        assert next_task.due_date is None  # Next occurrence should also have no due date