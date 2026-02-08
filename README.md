# Todo In-Memory Python Console App

A simple command-line todo application with intermediate features including priorities, tags, search, filter, and sort capabilities.

## Features

- Add, list, update, delete, and complete tasks
- Assign priorities (high, medium, low) to tasks
- Tag tasks with custom labels
- Search tasks by keyword
- Filter tasks by status, priority, and tags
- Sort tasks by creation date, priority, or title

## Setup

1. Ensure you have Python 3.13+ installed
2. Install dependencies using UV:
   ```
   uv sync
   ```

## Usage

### Basic Commands

- Add a task:
  ```
  python -m src.main add "Task Title" "Task Description"
  ```

- List all tasks:
  ```
  python -m src.main list
  ```

- Complete a task:
  ```
  python -m src.main complete 1
  ```

- Delete a task:
  ```
  python -m src.main delete 1
  ```

- Update a task:
  ```
  python -m src.main update 1 "New Title" "New Description"
  ```

### Intermediate Features

- Add a task with priority and tags:
  ```
  python -m src.main add "High Priority Task" "Description" --priority high --tag work,important
  ```

- List tasks with filters and sorting:
  ```
  python -m src.main list --status pending --priority high --sort title
  ```

- Search for tasks:
  ```
  python -m src.main search "keyword" --status pending --priority high
  ```

## Development

To run tests:
```
pytest
```

## Architecture

The application follows a modular architecture:
- `src/core/` - Core models and CRUD operations
- `src/features/` - Feature-specific logic (priorities_tags, query)
- `src/cli/` - Command-line interface components
- `src/ui/` - User interface components (colors, formatting, tables)

## Advanced Features

The application includes advanced features for task management:
- Recurring tasks with session-bound recurrence patterns (daily, weekly, monthly)
- Due date support with ISO 8601 datetime format
- Console-based reminder system that alerts on next user interaction after due time passes
- Combined filtering with due dates (e.g., `list --due-after "2026-02-10" --priority high`)
- Due date sorting (e.g., `list --sort due_date`)
- Cross-feature integration (recurring tasks with due dates, priorities, and tags)

## Session-Bound Limitations (Phase I Constraints)

This implementation operates under strict Phase I constraints:
- **In-Memory Storage Only**: All data is stored in memory and is lost when the application exits
- **Session-Bound Recurrence**: Recurring tasks only generate next occurrences while the application remains running; recurrence does not persist between application restarts
- **Console-Based Reminders**: Reminders only trigger during active user sessions and do not run in the background
- **CLI-Only Interface**: No web interface or GUI components; all interaction is through command line
- **Standard Library Only**: No external dependencies beyond Python's standard library

These limitations are intentional for Phase I and will be addressed in future phases with persistence mechanisms.

### Examples of Advanced Usage

- Add a recurring task with due date:
  ```
  python -m src.main add "Weekly planning" "Team sync" --recur weekly --due "2026-02-15T09:00:00"
  ```

- List tasks with due date filtering:
  ```
  python -m src.main list --due-after "2026-02-10" --sort due_date
  ```

- Search tasks with multiple filters:
  ```
  python -m src.main search "meeting" --priority high --due-before "2026-02-20"
  ```

## UI Enhancements

The application includes professional UI enhancements:
- Color-coded priority indicators (🔴 for high, 🟡 for medium, 🟢 for low)
- Structured table display for tasks with clear columns
- Enhanced error and success messages with appropriate formatting
- Accessible text-only mode for screen readers
- High contrast color options for improved visibility
- Recurrence indicators (R:daily, R:weekly, R:monthly) in task listings
- Due date display in task listings