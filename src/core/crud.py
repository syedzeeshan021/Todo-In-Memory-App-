from datetime import datetime
from typing import List, Optional
from .models import Task
from ..features.query import execute_query_pipeline


class TaskManager:
    """
    Manages in-memory storage of all tasks and handles all CRUD operations.
    """
    
    def __init__(self):
        """Initialize the TaskManager with an empty task list and ID counter."""
        self.tasks = {}
        self.next_id = 1
    
    def create_task(self, title: str, description: str = "", priority: str = "medium",
                   tags: List[str] = None, due_date: datetime = None, recurrence: str = None) -> Task:
        """
        Create a new task with the given parameters.

        Args:
            title: Task title
            description: Task description
            priority: Task priority ("high", "medium", "low")
            tags: List of tags for the task
            due_date: Due date for the task (optional)
            recurrence: Recurrence pattern ("daily", "weekly", "monthly") (optional)

        Returns:
            The newly created Task object
        """
        task_id = self.next_id
        self.next_id += 1

        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags or [],
            due_date=due_date,
            recurrence=recurrence
        )

        self.tasks[task_id] = task
        return task
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its ID.
        
        Args:
            task_id: The ID of the task to retrieve
            
        Returns:
            The Task object if found, None otherwise
        """
        return self.tasks.get(task_id)
    
    def list_tasks(self, status: str = "all", priority: str = "all",
                   tags: List[str] = None, sort_by: str = "created", 
                   due_before: datetime = None, due_after: datetime = None) -> List[Task]:
        """
        List tasks with optional filtering and sorting.

        Args:
            status: Filter by status ("all", "pending", "completed")
            priority: Filter by priority ("all", "high", "medium", "low")
            tags: Filter by tags (list of tags to match)
            sort_by: Sort by option ("created", "priority", "title", "due_date")
            due_before: Filter tasks due before this date (optional)
            due_after: Filter tasks due after this date (optional)

        Returns:
            List of Task objects matching the criteria
        """
        tasks = list(self.tasks.values())

        # Use the query pipeline to execute filters and sorting
        return execute_query_pipeline(
            tasks=tasks,
            status=status,
            priority=priority,
            tags=tags,
            keyword=None,  # No search keyword for list command
            sort_by=sort_by,
            due_before=due_before,
            due_after=due_after
        )
    
    def update_task(self, task_id: int, title: str = None, description: str = None,
                   priority: str = None, tags: List[str] = None, due_date: datetime = None, 
                   recurrence: str = None) -> Optional[Task]:
        """
        Update an existing task.

        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)
            tags: New tags (optional)
            due_date: New due date (optional)
            recurrence: New recurrence pattern (optional)

        Returns:
            Updated Task object if successful, None if task not found
        """
        task = self.get_task(task_id)
        if not task:
            return None

        task.update(title=title, description=description, priority=priority, tags=tags, 
                   due_date=due_date, recurrence=recurrence)
        return task
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by its ID.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            True if deletion was successful, False if task not found
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False
    
    def toggle_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggle the completion status of a task.

        Args:
            task_id: ID of the task to toggle

        Returns:
            Updated Task object if successful, None if task not found
        """
        task = self.get_task(task_id)
        if not task:
            return None

        # If the task has recurrence and is being marked as complete (going from incomplete to complete), generate next occurrence
        if task.recurrence and not task.completed:
            from ..features.recurrence import generate_next_occurrence
            next_task = generate_next_occurrence(task, self)
            
            # Add the next occurrence to the task manager
            self.tasks[next_task.id] = next_task

        task.completed = not task.completed
        task.updated_at = datetime.utcnow()
        return task
    
    def search_tasks(self, keyword: str, status: str = "all", priority: str = "all",
                     tags: List[str] = None, sort_by: str = "created",
                     due_before: datetime = None, due_after: datetime = None) -> List[Task]:
        """
        Search tasks by keyword in title and description with optional filters and sorting.

        Args:
            keyword: Keyword to search for in title and description
            status: Filter by status ("all", "pending", "completed")
            priority: Filter by priority ("all", "high", "medium", "low")
            tags: Filter by tags (list of tags to match)
            sort_by: Sort by option ("created", "priority", "title", "due_date")
            due_before: Filter tasks due before this date (optional)
            due_after: Filter tasks due after this date (optional)

        Returns:
            List of Task objects matching the search and criteria
        """
        tasks = list(self.tasks.values())

        # Use the query pipeline to execute search, filters and sorting
        return execute_query_pipeline(
            tasks=tasks,
            status=status,
            priority=priority,
            tags=tags,
            keyword=keyword,
            sort_by=sort_by,
            due_before=due_before,
            due_after=due_after
        )