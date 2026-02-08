# Data Model for Todo In-Memory Python Console App - Intermediate Features

## Task Entity

### Fields
- **id**: `int` - Unique identifier for the task within the session (auto-incremented)
- **title**: `str` - Task title (required, 1-200 characters)
- **description**: `str` - Task description (optional, max 1000 characters)
- **completed**: `bool` - Completion status (default: False)
- **priority**: `str` - Task priority level ("high", "medium", "low") (default: "medium")
- **tags**: `list[str]` - List of tags associated with the task (default: [])
- **created_at**: `datetime` - Timestamp of task creation (UTC)
- **updated_at**: `datetime` - Timestamp of last task update (UTC)

### Validation Rules
- **id**: Auto-generated, positive integer
- **title**: Required, trimmed of leading/trailing whitespace, 1-200 characters after trimming
- **description**: Optional, trimmed of leading/trailing whitespace, max 1000 characters after trimming
- **completed**: Boolean value only
- **priority**: Must be one of "high", "medium", "low" (case-insensitive, normalized to lowercase)
- **tags**: List of strings, each tag split by commas from input, whitespace trimmed, empty tags discarded
- **created_at**: Automatically set on creation, UTC timezone
- **updated_at**: Automatically updated on any modification, UTC timezone

### State Transitions
- **Creation**: New task with default values for optional fields
- **Update**: Modify title, description, priority, or tags; update `updated_at`
- **Toggle Completion**: Change `completed` status; update `updated_at`
- **Deletion**: Remove task from storage

## Task Manager

### Responsibilities
- Maintain in-memory storage of all tasks
- Generate unique IDs for new tasks
- Handle all CRUD operations
- Apply filters, sorting, and search operations
- Maintain data integrity and validation

### Methods
- `create_task(title: str, description: str, priority: str, tags: list[str]) -> Task`
- `get_task(task_id: int) -> Task | None`
- `list_tasks(status: str, priority: str, tags: list[str], sort_by: str) -> list[Task]`
- `update_task(task_id: int, title: str, description: str, priority: str, tags: list[str]) -> Task | None`
- `delete_task(task_id: int) -> bool`
- `toggle_completion(task_id: int) -> Task | None`
- `search_tasks(keyword: str, status: str, priority: str, tags: list[str], sort_by: str) -> list[Task]`

## CLI Command Models

### Add Command
- **Arguments**: title (str), description (str)
- **Options**: --priority (str), --tag (str)
- **Validation**: Same as Task entity validation

### List Command
- **Options**: --status (str), --priority (str), --tag (str), --sort (str)
- **Validation**: Options must be valid values

### Search Command
- **Arguments**: keyword (str)
- **Options**: --status (str), --priority (str), --tag (str), --sort (str)
- **Validation**: Same as List Command

### Update Command
- **Arguments**: id (int), title (str), description (str)
- **Options**: --priority (str), --tag (str)
- **Validation**: Same as Task entity validation