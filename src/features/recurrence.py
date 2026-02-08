"""
Module for handling recurring tasks in the todo application.
This includes recurrence pattern calculation and next occurrence generation.
"""
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from ..core.models import Task


def calculate_next_due(original_due: Optional[datetime], pattern: str) -> Optional[datetime]:
    """
    Calculate the next due date based on the original due date and recurrence pattern.

    Args:
        original_due: The original due date
        pattern: The recurrence pattern ('daily', 'weekly', 'monthly')

    Returns:
        The next due date based on the pattern, or None if original due is None
    """
    if original_due is None:
        return None

    if pattern == "daily":
        return original_due + timedelta(days=1)
    elif pattern == "weekly":
        return original_due + timedelta(days=7)
    elif pattern == "monthly":
        # Simple implementation: add 30 days for monthly recurrence
        # This is an intentional Phase I limitation (not calendar-aware)
        return original_due + timedelta(days=30)
    else:
        raise ValueError(f"Invalid recurrence pattern: {pattern}")


def generate_next_occurrence(task: Task, task_manager) -> Task:
    """
    Generate the next occurrence of a recurring task.

    Args:
        task: The completed recurring task
        task_manager: The TaskManager instance to get next ID from

    Returns:
        A new Task instance with the next occurrence details
    """
    # Calculate next due date if the original task had one
    next_due_date = calculate_next_due(task.due_date, task.recurrence)

    # Get the next ID from the task manager and increment it
    task_id = task_manager.next_id
    task_manager.next_id += 1

    # Create a new task with the same properties as the original
    next_task = Task(
        id=task_id,
        title=task.title,
        description=task.description,
        completed=False,  # New occurrence is not completed
        priority=task.priority,  # Preserve original priority
        tags=task.tags[:],  # Copy tags list
        due_date=next_due_date,  # Calculate next due date based on pattern
        recurrence=task.recurrence,  # Preserve recurrence pattern
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    return next_task