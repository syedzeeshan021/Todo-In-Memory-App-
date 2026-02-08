from datetime import datetime
from typing import List, Optional


class Task:
    """
    Represents a task in the todo application with enhanced fields for priorities, tags, due dates, and recurrence.
    """

    def __init__(self, id: int, title: str, description: str = "", completed: bool = False,
                 priority: str = "medium", tags: List[str] = None, due_date: datetime = None, 
                 recurrence: str = None, created_at: datetime = None, updated_at: datetime = None):
        """
        Initialize a Task instance.

        Args:
            id: Unique identifier for the task within the session
            title: Task title (required, 1-200 characters)
            description: Task description (optional, max 1000 characters)
            completed: Completion status (default: False)
            priority: Task priority level ("high", "medium", "low") (default: "medium")
            tags: List of tags associated with the task (default: [])
            due_date: Due date/time for the task (default: None)
            recurrence: Recurrence pattern ("daily", "weekly", "monthly", default: None)
            created_at: Timestamp of task creation (UTC)
            updated_at: Timestamp of last task update (UTC)
        """
        self.id = id
        self.title = self._validate_and_normalize_title(title)
        self.description = self._validate_and_normalize_description(description)
        self.completed = completed
        self.priority = self._validate_and_normalize_priority(priority)
        self.tags = self._validate_and_normalize_tags(tags or [])
        self.due_date = self._validate_and_normalize_due_date(due_date)
        self.recurrence = self._validate_and_normalize_recurrence(recurrence)
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    def _validate_and_normalize_title(self, title: str) -> str:
        """Validate and normalize the title."""
        if not isinstance(title, str):
            raise ValueError("Title must be a string")
        
        normalized_title = title.strip()
        
        if not normalized_title:
            raise ValueError("Title cannot be empty after trimming")
        
        if len(normalized_title) > 200:
            raise ValueError(f"Title exceeds 200 characters: {len(normalized_title)} characters")
        
        return normalized_title

    def _validate_and_normalize_description(self, description: str) -> str:
        """Validate and normalize the description."""
        if not isinstance(description, str):
            raise ValueError("Description must be a string")
        
        normalized_desc = description.strip()
        
        if len(normalized_desc) > 1000:
            raise ValueError(f"Description exceeds 1000 characters: {len(normalized_desc)} characters")
        
        return normalized_desc

    def _validate_and_normalize_priority(self, priority: str) -> str:
        """Validate and normalize the priority."""
        if not isinstance(priority, str):
            raise ValueError("Priority must be a string")
        
        normalized_priority = priority.lower().strip()
        
        if normalized_priority not in ["high", "medium", "low"]:
            raise ValueError(f"Invalid priority: '{priority}'. Must be one of 'high', 'medium', 'low'")
        
        return normalized_priority

    def _validate_and_normalize_tags(self, tags: List[str]) -> List[str]:
        """Validate and normalize the tags."""
        if not isinstance(tags, list):
            raise ValueError("Tags must be a list")
        
        normalized_tags = []
        for tag in tags:
            if not isinstance(tag, str):
                raise ValueError(f"Tag must be a string: {tag}")

            normalized_tag = tag.strip()
            if normalized_tag:  # Only add non-empty tags
                normalized_tags.append(normalized_tag)

        return normalized_tags

    def _validate_and_normalize_due_date(self, due_date: datetime) -> Optional[datetime]:
        """Validate and normalize the due date."""
        if due_date is None:
            return None

        if not isinstance(due_date, datetime):
            raise ValueError("Due date must be a datetime object or None")

        # For Phase I, we'll accept any datetime (validation of future dates can be added later)
        return due_date

    def _validate_and_normalize_recurrence(self, recurrence: str) -> Optional[str]:
        """Validate and normalize the recurrence pattern."""
        if recurrence is None:
            return None

        if not isinstance(recurrence, str):
            raise ValueError("Recurrence must be a string or None")

        normalized_recurrence = recurrence.lower().strip()

        if normalized_recurrence not in ["daily", "weekly", "monthly"]:
            raise ValueError(f"Invalid recurrence pattern: '{recurrence}'. Must be one of 'daily', 'weekly', 'monthly'")

        return normalized_recurrence

    def update(self, title: str = None, description: str = None, priority: str = None,
               tags: List[str] = None, completed: bool = None, due_date: datetime = None, 
               recurrence: str = None):
        """
        Update task properties.

        Args:
            title: New title (optional)
            description: New description (optional)
            priority: New priority (optional)
            tags: New tags (optional)
            completed: New completion status (optional)
            due_date: New due date (optional)
            recurrence: New recurrence pattern (optional)
        """
        if title is not None:
            self.title = self._validate_and_normalize_title(title)
        if description is not None:
            self.description = self._validate_and_normalize_description(description)
        if priority is not None:
            self.priority = self._validate_and_normalize_priority(priority)
        if tags is not None:
            self.tags = self._validate_and_normalize_tags(tags)
        if completed is not None:
            self.completed = completed
        if due_date is not None:
            self.due_date = self._validate_and_normalize_due_date(due_date)
        if recurrence is not None:
            self.recurrence = self._validate_and_normalize_recurrence(recurrence)

        self.updated_at = datetime.utcnow()

    def __repr__(self):
        return f"Task(id={self.id}, title='{self.title}', completed={self.completed}, priority='{self.priority}', tags={self.tags}, due_date={self.due_date}, recurrence={self.recurrence})"