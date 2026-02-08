"""
Module for handling due date reminders in the todo application.
This includes checking for overdue tasks and upcoming due date notifications.
"""
from datetime import datetime, timedelta
from typing import List
from ..core.models import Task


def check_for_reminders(tasks: List[Task]) -> List[str]:
    """
    Check all tasks for due date reminders.
    
    Args:
        tasks: List of all tasks to check
        
    Returns:
        List of reminder messages to display
    """
    reminders = []
    current_time = datetime.utcnow()
    
    for task in tasks:
        if task.completed:
            continue  # Skip completed tasks
            
        if task.due_date is None:
            continue  # Skip tasks without due dates
            
        # Check if task is overdue
        if current_time > task.due_date:
            time_diff = current_time - task.due_date
            days = time_diff.days
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes, _ = divmod(remainder, 60)
            
            if days > 0:
                reminder = f'[REMINDER] "{task.title}" was due {days} day(s) ago!'
            elif hours > 0:
                reminder = f'[REMINDER] "{task.title}" was due {hours} hour(s) ago!'
            else:
                reminder = f'[REMINDER] "{task.title}" was due {minutes} minute(s) ago!'
                
            reminders.append(reminder)
        else:
            # Check if task is due soon (within 24 hours)
            time_until_due = task.due_date - current_time
            if time_until_due <= timedelta(hours=24):
                days = time_until_due.days
                hours, remainder = divmod(time_until_due.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                
                if days > 0:
                    reminder = f'[REMINDER] "{task.title}" due in {days} day(s)!'
                elif hours > 0:
                    reminder = f'[REMINDER] "{task.title}" due in {hours} hour(s)!'
                else:
                    reminder = f'[REMINDER] "{task.title}" due in {minutes} minute(s)!'
                    
                reminders.append(reminder)
    
    return reminders


def format_reminder_message(task_title: str, time_info: str, is_overdue: bool) -> str:
    """
    Format a reminder message consistently.
    
    Args:
        task_title: Title of the task
        time_info: Time-related information
        is_overdue: Whether the task is overdue
        
    Returns:
        Formatted reminder message
    """
    if is_overdue:
        return f'[REMINDER] "{task_title}" was {time_info}'
    else:
        return f'[REMINDER] "{task_title}" {time_info}'