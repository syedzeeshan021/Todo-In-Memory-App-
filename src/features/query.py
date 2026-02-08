"""
Module for handling search, filter, and sort operations in the todo application.
This includes the query execution pipeline that processes filters, search, and sorting.
"""

from datetime import datetime
from typing import List
from ..core.models import Task


def filter_tasks(tasks: List[Task], status: str = "all", priority: str = "all",
                tags: List[str] = None, due_before: datetime = None, due_after: datetime = None) -> List[Task]:
    """
    Filter tasks based on status, priority, tags, and due dates.

    Args:
        tasks: List of tasks to filter
        status: Filter by status ("all", "pending", "completed")
        priority: Filter by priority ("all", "high", "medium", "low")
        tags: Filter by tags (list of tags to match using OR logic)
        due_before: Filter tasks due before this date (optional)
        due_after: Filter tasks due after this date (optional)

    Returns:
        List of tasks that match the filter criteria
    """
    filtered_tasks = tasks.copy()

    # Apply status filter
    if status != "all":
        if status == "pending":
            filtered_tasks = [task for task in filtered_tasks if not task.completed]
        elif status == "completed":
            filtered_tasks = [task for task in filtered_tasks if task.completed]

    # Apply priority filter
    if priority != "all":
        filtered_tasks = [task for task in filtered_tasks if task.priority == priority]

    # Apply tag filter
    if tags:
        # For tag filtering, implement OR logic (task has one or more of the specified tags)
        filtered_tasks = [
            task for task in filtered_tasks
            if any(requested_tag in task.tags for requested_tag in tags)
        ]

    # Apply due date filters
    if due_before:
        filtered_tasks = [task for task in filtered_tasks if task.due_date and task.due_date <= due_before]

    if due_after:
        filtered_tasks = [task for task in filtered_tasks if task.due_date and task.due_date >= due_after]

    return filtered_tasks


def search_tasks(tasks: List[Task], keyword: str) -> List[Task]:
    """
    Search tasks by keyword in title, description, and due date (if it's a date string).

    Args:
        tasks: List of tasks to search
        keyword: Keyword to search for

    Returns:
        List of tasks that match the search keyword
    """
    if not keyword:
        return tasks

    keyword_lower = keyword.lower()
    return [
        task for task in tasks
        if keyword_lower in task.title.lower() or 
           keyword_lower in task.description.lower() or
           (task.due_date and keyword_lower in task.due_date.isoformat().lower())
    ]


def sort_tasks(tasks: List[Task], sort_by: str = "created") -> List[Task]:
    """
    Sort tasks based on the specified criteria.

    Args:
        tasks: List of tasks to sort
        sort_by: Sort by option ("created", "priority", "title", "due_date")

    Returns:
        List of tasks sorted according to the specified criteria
    """
    if sort_by == "priority":
        # Sort by priority (high -> medium -> low) then by creation time (newest first)
        priority_order = {"high": 0, "medium": 1, "low": 2}
        return sorted(tasks, key=lambda t: (priority_order[t.priority], -t.created_at.timestamp()))
    elif sort_by == "title":
        # Sort by title (case-insensitive)
        return sorted(tasks, key=lambda t: t.title.lower())
    elif sort_by == "due_date":
        # Sort by due date (soonest first), tasks without due dates appear last
        def due_date_key(task):
            if task.due_date is None:
                # Use a far future date to push tasks without due dates to the end
                return datetime.max
            return task.due_date
        return sorted(tasks, key=due_date_key)
    elif sort_by == "created":
        # Sort by creation time (newest first)
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)
    else:
        # Default to creation time sorting
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)


def execute_query_pipeline(tasks: List[Task], status: str = "all", priority: str = "all",
                         tags: List[str] = None, keyword: str = None,
                         sort_by: str = "created", due_before: datetime = None, 
                         due_after: datetime = None) -> List[Task]:
    """
    Execute the full query pipeline: filter → search → sort.

    Args:
        tasks: List of tasks to process
        status: Filter by status
        priority: Filter by priority
        tags: Filter by tags
        keyword: Search keyword
        sort_by: Sort by option
        due_before: Filter tasks due before this date (optional)
        due_after: Filter tasks due after this date (optional)

    Returns:
        List of tasks processed through the full pipeline
    """
    # Step 1: Apply filters
    filtered_tasks = filter_tasks(tasks, status, priority, tags, due_before, due_after)

    # Step 2: Apply search
    searched_tasks = search_tasks(filtered_tasks, keyword)

    # Step 3: Apply sorting
    sorted_tasks = sort_tasks(searched_tasks, sort_by)

    return sorted_tasks