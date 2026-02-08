# API Contract for Todo In-Memory Python Console App

## Overview
This document describes the API contracts for the CLI commands of the Todo In-Memory Python Console App with intermediate features.

## Command Structure
```
python -m src.main <command> [arguments] [options]
```

## Commands

### 1. Add Task
**Usage**: `python -m src.main add <title> <description> [--priority <level>] [--tag <tags>]`

**Arguments**:
- `title`: Task title (string, required)
- `description`: Task description (string, required)

**Options**:
- `--priority`: Task priority level (string, optional, values: "high", "medium", "low", default: "medium")
- `--tag`: Comma-separated tags (string, optional, format: "tag1,tag2,tag3")

**Response**:
- Success: Task created with unique ID
- Error: `[ERROR] <error message>`

**Example**:
```
python -m src.main add "Complete project" "Finish the project documentation" --priority high --tag work,important
```

### 2. List Tasks
**Usage**: `python -m src.main list [--status <status>] [--priority <level>] [--tag <value>] [--sort <option>]`

**Options**:
- `--status`: Filter by status (string, optional, values: "all", "pending", "completed", default: "all")
- `--priority`: Filter by priority (string, optional, values: "all", "high", "medium", "low", default: "all")
- `--tag`: Filter by tag (string, optional, can be specified multiple times for OR condition)
- `--sort`: Sort by option (string, optional, values: "created", "priority", "title", default: "created")

**Response**:
- Success: List of tasks matching the criteria
- Error: `[ERROR] <error message>`

**Example**:
```
python -m src.main list --status pending --priority high --tag work --sort priority
```

### 3. Search Tasks
**Usage**: `python -m src.main search <keyword> [--status <status>] [--priority <level>] [--tag <value>] [--sort <option>]`

**Arguments**:
- `keyword`: Search term (string, required)

**Options**:
- `--status`: Filter by status (string, optional, values: "all", "pending", "completed", default: "all")
- `--priority`: Filter by priority (string, optional, values: "all", "high", "medium", "low", default: "all")
- `--tag`: Filter by tag (string, optional, can be specified multiple times for OR condition)
- `--sort`: Sort by option (string, optional, values: "created", "priority", "title", default: "created")

**Response**:
- Success: List of tasks matching the keyword and criteria
- Error: `[ERROR] <error message>`

**Example**:
```
python -m src.main search "meeting" --status pending --priority high
```

### 4. Update Task
**Usage**: `python -m src.main update <id> <title> <description> [--priority <level>] [--tag <tags>]`

**Arguments**:
- `id`: Task ID (integer, required)
- `title`: Task title (string, required)
- `description`: Task description (string, required)

**Options**:
- `--priority`: Task priority level (string, optional, values: "high", "medium", "low", preserves existing if omitted)
- `--tag`: Comma-separated tags (string, optional, format: "tag1,tag2,tag3", preserves existing if omitted)

**Response**:
- Success: Task updated successfully
- Error: `[ERROR] <error message>`

**Example**:
```
python -m src.main update 1 "Updated title" "Updated description" --priority low --tag personal
```

### 5. Complete Task
**Usage**: `python -m src.main complete <id>`

**Arguments**:
- `id`: Task ID (integer, required)

**Response**:
- Success: Task marked as completed
- Error: `[ERROR] <error message>`

**Example**:
```
python -m src.main complete 1
```

### 6. Delete Task
**Usage**: `python -m src.main delete <id>`

**Arguments**:
- `id`: Task ID (integer, required)

**Response**:
- Success: Task deleted
- Error: `[ERROR] <error message>`

**Example**:
```
python -m src.main delete 1
```

### 7. View Task
**Usage**: `python -m src.main view <id>`

**Arguments**:
- `id`: Task ID (integer, required)

**Response**:
- Success: Task details
- Error: `[ERROR] <error message>`

**Example**:
```
python -m src.main view 1
```

## Error Handling
All errors follow the format: `[ERROR] <descriptive message>`

Common errors:
- Invalid task ID: `[ERROR] Task <id> not found`
- Invalid priority: `[ERROR] Invalid priority: '<value>'. Must be high/medium/low`
- Invalid status: `[ERROR] Invalid status: '<value>'. Must be all/pending/completed`
- Invalid sort option: `[ERROR] Invalid sort option: '<value>'. Must be created/priority/title`
- Missing arguments: `[ERROR] Missing required argument: <argument>`

## Validation Rules
- Title: 1-200 characters after whitespace trimming
- Description: Max 1000 characters after whitespace trimming
- Priority: Must be one of "high", "medium", "low" (case-insensitive)
- Tags: Comma-separated, whitespace trimmed, empty tags ignored
- ID: Positive integer corresponding to existing task