# Quickstart Guide for Todo In-Memory Python Console App

## Prerequisites
- Python 3.13+
- UV (for environment management)

## Setup
1. Clone the repository
2. Install dependencies using UV:
   ```
   uv venv
   uv pip install -r requirements.txt
   ```
   Or if using pyproject.toml:
   ```
   uv sync
   ```

## Running the Application
```
python -m src.main
```

## Basic Commands
- **Add a task**: 
  ```
  python -m src.main add "Task Title" "Task Description"
  ```
- **List all tasks**:
  ```
  python -m src.main list
  ```
- **Complete a task**:
  ```
  python -m src.main complete 1
  ```
- **Delete a task**:
  ```
  python -m src.main delete 1
  ```
- **Update a task**:
  ```
  python -m src.main update 1 "New Title" "New Description"
  ```

## Intermediate Features Commands

### Adding Tasks with Priority and Tags
```
python -m src.main add "High Priority Task" "Description" --priority high --tag work,important
```

### Listing Tasks with Filters and Sorting
```
# List pending tasks sorted by priority
python -m src.main list --status pending --sort priority

# List high priority tasks with 'work' tag
python -m src.main list --priority high --tag work

# List tasks with multiple tags (OR condition)
python -m src.main list --tag work --tag urgent

# Sort by title
python -m src.main list --sort title
```

### Searching Tasks
```
# Search for tasks containing 'meeting'
python -m src.main search "meeting"

# Search with filters
python -m src.main search "meeting" --status pending --priority high

# Search with multiple tags (OR condition)
python -m src.main search "project" --tag work --tag urgent
```

### Available Options
- **Status**: `all`, `pending`, `completed` (default: `all`)
- **Priority**: `all`, `high`, `medium`, `low` (default: `all`)
- **Sort**: `created`, `priority`, `title` (default: `created`)
- **Tag**: Any tag name (can specify multiple tags for OR condition)

## Help
Get help for any command:
```
python -m src.main --help
python -m src.main add --help
python -m src.main list --help
python -m src.main search --help
```

## Error Messages
All error messages follow the format: `[ERROR] Description`

## Notes
- All data is stored in memory only and will be lost when the application exits
- Task IDs are stable within a session but reset on application restart
- All basic commands work without the new flags to maintain backward compatibility