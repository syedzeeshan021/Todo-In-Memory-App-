"""
Unit tests for reminder functionality in the todo application.
"""
import pytest
from datetime import datetime, timedelta
from src.core.models import Task
from src.features.reminders import check_for_reminders


class TestReminders:
    """Test cases for reminder functionality."""
    
    def test_check_for_reminders_no_overdue_tasks(self):
        """Test that no reminders are returned when no tasks are overdue."""
        # Use a future date far enough in the future that it won't be considered "upcoming" (within 24 hours)
        future_due = datetime.utcnow() + timedelta(days=7)
        tasks = [
            Task(
                id=1,
                title="Future task",
                description="Task due in a week",
                completed=False,
                due_date=future_due,
                priority="medium",
                tags=["test"],
                recurrence=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        reminders = check_for_reminders(tasks)
        assert len(reminders) == 0
    
    def test_check_for_reminders_overdue_task(self):
        """Test that overdue tasks generate reminders."""
        past_due = datetime.utcnow() - timedelta(hours=2)
        tasks = [
            Task(
                id=1,
                title="Overdue task",
                description="Task that was due 2 hours ago",
                completed=False,
                due_date=past_due,
                priority="high",
                tags=["urgent"],
                recurrence=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        reminders = check_for_reminders(tasks)
        assert len(reminders) == 1
        assert "Overdue task" in reminders[0]
        assert "was due" in reminders[0]
        assert "2 hour(s)" in reminders[0]
    
    def test_check_for_reminders_completed_task(self):
        """Test that completed tasks do not generate reminders."""
        past_due = datetime.utcnow() - timedelta(hours=1)
        tasks = [
            Task(
                id=1,
                title="Completed task",
                description="Task that was completed",
                completed=True,  # Task is completed
                due_date=past_due,
                priority="high",
                tags=["urgent"],
                recurrence=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        reminders = check_for_reminders(tasks)
        assert len(reminders) == 0
    
    def test_check_for_reminders_task_without_due_date(self):
        """Test that tasks without due dates do not generate reminders."""
        tasks = [
            Task(
                id=1,
                title="Task without due date",
                description="Just a regular task",
                completed=False,
                due_date=None,  # No due date
                priority="medium",
                tags=["test"],
                recurrence=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        reminders = check_for_reminders(tasks)
        assert len(reminders) == 0
    
    def test_check_for_reminders_upcoming_due_soon(self):
        """Test that tasks due soon (within 24 hours) generate reminders."""
        due_soon = datetime.utcnow() + timedelta(hours=6)
        tasks = [
            Task(
                id=1,
                title="Upcoming task",
                description="Task due in 6 hours",
                completed=False,
                due_date=due_soon,
                priority="medium",
                tags=["test"],
                recurrence=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        reminders = check_for_reminders(tasks)
        assert len(reminders) == 1
        assert "Upcoming task" in reminders[0]
        assert "due in" in reminders[0]
        # The reminder message might show a slightly different time due to processing delays
        # So we'll check for the presence of "hour(s)" rather than the exact number
        assert "hour(s)" in reminders[0] or "hours" in reminders[0]
    
    def test_check_for_reminders_multiple_tasks(self):
        """Test that multiple overdue and upcoming tasks generate multiple reminders."""
        past_due = datetime.utcnow() - timedelta(hours=3)
        due_soon = datetime.utcnow() + timedelta(hours=12)
        future_due = datetime.utcnow() + timedelta(days=2)
        
        tasks = [
            Task(
                id=1,
                title="Overdue task",
                description="Task overdue by 3 hours",
                completed=False,
                due_date=past_due,
                priority="high",
                tags=["urgent"],
                recurrence=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Task(
                id=2,
                title="Upcoming task",
                description="Task due in 12 hours",
                completed=False,
                due_date=due_soon,
                priority="medium",
                tags=["test"],
                recurrence=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            ),
            Task(
                id=3,
                title="Future task",
                description="Task due in 2 days",
                completed=False,
                due_date=future_due,
                priority="low",
                tags=["later"],
                recurrence=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
        ]
        
        reminders = check_for_reminders(tasks)
        assert len(reminders) == 2  # Only overdue and upcoming tasks should generate reminders
        reminder_titles = [r.split('"')[1] for r in reminders]  # Extract task titles from reminders
        assert "Overdue task" in reminder_titles
        assert "Upcoming task" in reminder_titles
        assert "Future task" not in reminder_titles