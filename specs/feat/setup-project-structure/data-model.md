# Data Model for Todo In-Memory Python Console App (Advanced Level)

## Task Entity

### Fields
- **id**: `int` - Unique identifier for the task within the session (auto-incremented)
- **title**: `str` - Task title (required, 1-200 characters)
- **description**: `str` - Task description (optional, max 1000 characters)
- **completed**: `bool` - Completion status (default: False)
- **priority**: `str` - Task priority level ("high", "medium", "low") (default: "medium")
- **tags**: `list[str]` - List of tags associated with the task (default: [])
- **due_date**: `datetime | None` - Due date/time for the task (default: None)
- **recurrence**: `str | None` - Recurrence pattern ("daily", "weekly", "monthly") (default: None)
- **created_at**: `datetime` - Timestamp of task creation (UTC)
- **updated_at**: `datetime` - Timestamp of last task update (UTC)

### Validation Rules
- **id**: Auto-generated, positive integer
- **title**: Required, trimmed of leading/trailing whitespace, 1-200 characters after trimming
- **description**: Optional, trimmed of leading/trailing whitespace, max 1000 characters after trimming
- **completed**: Boolean value only
- **priority**: Must be one of "high", "medium", "low" (case-insensitive, normalized to lowercase)
- **tags**: List of strings, each tag split by commas from input, whitespace trimmed, empty tags discarded
- **due_date**: Must be a valid ISO 8601 datetime string, converted to UTC for storage
- **recurrence**: Must be one of "daily", "weekly", "monthly" (case-insensitive, normalized to lowercase) or None
- **created_at**: Automatically set on creation, UTC timezone
- **updated_at**: Automatically updated on any modification, UTC timezone

### State Transitions
- **Creation**: New task with default values for optional fields, due_date=None, recurrence=None
- **Update**: Modify title, description, priority, tags, due_date, or recurrence; update `updated_at`
- **Toggle Completion**: Change `completed` status; update `updated_at`; if recurring, generate next occurrence
- **Deletion**: Remove task from storage

## Task Manager

### Responsibilities
- Maintain in-memory storage of all tasks
- Generate unique IDs for new tasks
- Handle all CRUD operations
- Apply filters, sorting, and search operations
- Manage recurrence: generate next occurrences when recurring tasks are completed
- Manage reminders: check for overdue tasks before command output
- Maintain data integrity and validation

### Methods
- `create_task(title: str, description: str, priority: str, tags: list[str], due_date: datetime | None, recurrence: str | None) -> Task`
- `get_task(task_id: int) -> Task | None`
- `list_tasks(status: str, priority: str, tags: list[str], due_before: datetime | None, due_after: datetime | None, sort_by: str) -> list[Task]`
- `update_task(task_id: int, title: str, description: str, priority: str, tags: list[str], due_date: datetime | None, recurrence: str | None) -> Task | None`
- `delete_task(task_id: int) -> bool`
- `toggle_completion(task_id: int) -> Task | None`
- `search_tasks(keyword: str, status: str, priority: str, tags: list[str], due_before: datetime | None, due_after: datetime | None, sort_by: str) -> list[Task]`
- `generate_next_occurrence(task: Task) -> Task | None`
- `check_reminders() -> list[Task]`

## Recurrence Entity

### Fields
- **original_task_id**: `int` - ID of the original task that spawned this occurrence
- **pattern**: `str` - Recurrence pattern ("daily", "weekly", "monthly")
- **interval_days**: `int` - Interval in days based on pattern (1, 7, or 30)

### Methods
- `calculate_next_due(original_due: datetime, pattern: str) -> datetime`
- `generate_next_occurrence(task: Task) -> Task`

## CLI Command Models

### Add Command
- **Arguments**: title (str), description (str)
- **Options**: --priority (str), --tag (str), --due (str), --recur (str)
- **Validation**: Same as Task entity validation

### List Command
- **Options**: --status (str), --priority (str), --tag (str), --due-before (str), --due-after (str), --sort (str)
- **Validation**: Options must be valid values

### Search Command
- **Arguments**: keyword (str)
- **Options**: --status (str), --priority (str), --tag (str), --due-before (str), --due-after (str), --sort (str)
- **Validation**: Same as List Command

### Update Command
- **Arguments**: id (int), title (str), description (str)
- **Options**: --priority (str), --tag (str), --due (str), --recur (str)
- **Validation**: Same as Task entity validation