# Quickstart Guide: Todo In-Memory Python Console App (Advanced Level)

## Setup

1. Ensure Python 3.13+ is installed
2. Install dependencies using UV:
   ```bash
   uv sync
   ```
   Or if using pyproject.toml:
   ```bash
   uv pip install -e .
   ```

## Running the Application

```bash
python -m src.main
```

## Basic Commands (Unchanged from Basic Level)
- **Add a task**: 
  ```bash
  python -m src.main add "Task Title" "Task Description"
  ```
- **List all tasks**:
  ```bash
  python -m src.main list
  ```
- **Complete a task**:
  ```bash
  python -m src.main complete 1
  ```
- **Delete a task**:
  ```bash
  python -m src.main delete 1
  ```
- **Update a task**:
  ```bash
  python -m src.main update 1 "New Title" "New Description"
  ```

## Intermediate Features (Unchanged from Intermediate Level)
- **Add with priority and tags**:
  ```bash
  python -m src.main add "High Priority Task" "Description" --priority high --tag work,urgent
  ```
- **Filter and sort**:
  ```bash
  python -m src.main list --priority high --sort title
  ```
- **Search**:
  ```bash
  python -m src.main search "keyword" --status pending
  ```

## Advanced Features (New in Advanced Level)

### Adding Tasks with Due Dates and Recurrence
```bash
# Add task with due date
python -m src.main add "Submit report" "Quarterly financial report" --due "2026-02-15T17:00:00"

# Add recurring task
python -m src.main add "Team standup" "Weekly team sync" --recur weekly

# Add task with both due date and recurrence
python -m src.main add "Pay bills" "Monthly utility payments" --due "2026-02-28T23:59:00" --recur monthly
```

### Filtering and Sorting by Due Date
```bash
# List tasks due before a certain date
python -m src.main list --due-before "2026-02-20"

# List tasks due after a certain date
python -m src.main list --due-after "2026-02-10"

# Sort tasks by due date
python -m src.main list --sort due_date

# Combine with other filters
python -m src.main list --priority high --due-before "2026-02-20" --sort due_date
```

### Searching with Due Dates
```bash
# Search tasks with due date filters
python -m src.main search "report" --due-after "2026-02-01" --sort due_date
```

### Recurrence Behavior
When you complete a recurring task, the system automatically generates the next occurrence:
```bash
python -m src.main complete 5  # If task 5 was recurring, next occurrence is created
```

### Reminder System
When you run any command and have overdue tasks, the system will display reminders before the command output:
```
[REMINDER] "Submit report" was due 2 hours ago!
[REMINDER] "Team standup" due in 30 minutes!
```

## Important Limitations (Phase I Constraints)

1. **Session-Bound Recurrence**: Recurring tasks only generate next occurrences while the application remains running. When you exit the application, recurrence schedules are not preserved.

2. **Session-Bound Reminders**: Due date reminders only trigger during active sessions. They do not run in the background or persist between application restarts.

3. **In-Memory Storage**: All tasks are stored only in memory and will be lost when the application exits.

4. **UTC Timezone**: All due dates are stored in UTC. When entering due dates, use ISO 8601 format with timezone information or ensure your local time is properly converted to UTC.

## Help
Get help for any command:
```bash
python -m src.main --help
python -m src.main add --help
python -m src.main list --help
python -m src.main search --help
```

## Error Messages
All error messages follow the format: `[ERROR] Description`

## Demo Script
For the 90-second demo showcasing all feature levels:
1. First 20s: Basic CRUD operations
2. Next 30s: Intermediate features (priorities, tags, search, filter, sort)
3. Final 40s: Advanced features (recurring tasks, due dates, reminders)