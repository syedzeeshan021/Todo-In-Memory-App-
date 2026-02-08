# Todo In-Memory Python Console App Specification (Intermediate Level)

## 1. User Journeys

### Journey 1: Organizing Tasks with Priorities and Tags
- User adds task "Prepare presentation" with priority "high" and tags "work,urgent"
- User adds task "Buy groceries" with default priority (medium) and tag "personal"
- User lists all tasks → sees priority indicators ([!] for high) and tags displayed
- User filters to show only high-priority tasks → sees only presentation task
- User filters to show personal tasks → sees only groceries task

### Journey 2: Finding Specific Tasks Efficiently
- User has 15 tasks with mixed priorities/tags/statuses
- User searches "meeting" → returns tasks containing "meeting" in title/description
- User searches "meeting" with --status pending → returns only pending meeting tasks
- User searches "meeting" with --priority high --tag work → returns high-priority work meetings only

### Journey 3: Managing Task Visibility Through Sorting
- User lists tasks sorted by priority → high priority first, then medium, then low
- User lists tasks sorted by title → alphabetical order (case-insensitive)
- User combines sort with filters: "list --priority high --sort title"
- Default sort remains chronological (newest first) when no --sort flag provided

### Journey 4: Backward Compatibility Verification
- User executes basic commands WITHOUT intermediate flags:
  - `add "Simple task" "No priority/tag"`
  - `list` (no flags)
  - `complete 1`
  - `delete 2`
- All commands function identically to basic-level implementation
- No new required fields or breaking changes to existing syntax

## 2. Functional Requirements

### FR-01: Priority Assignment
- Priority is OPTIONAL during task creation/update
- Three valid values: "high", "medium", "low" (case-insensitive input accepted)
- Default priority: "medium" when not specified
- Display indicators in listings:
  - `[!]` prefix for high priority tasks
  - `[~]` prefix for medium priority tasks (optional but recommended)
  - `[ ]` prefix for low priority tasks
- Priority values stored normalized to lowercase

### FR-02: Tag Management
- Tags are OPTIONAL comma-separated strings (e.g., "work,urgent,team")
- Whitespace around commas normalized (trim spaces)
- Empty tags ("", " ") treated as no tags
- Tags displayed after description in parentheses: `(work, personal)`
- Case-sensitive storage but case-insensitive matching for filters

### FR-03: Search Functionality
- Command: `search <keyword>`
- Searches title AND description fields
- Case-insensitive partial match (e.g., "meet" matches "meeting")
- Special characters treated literally (no regex interpretation)
- Returns empty list when no matches found (with friendly message)

### FR-04: Filter Combinations
- Filters combinable on `list` and `search` commands:
  - `--status [all|pending|completed]` (default: all)
  - `--priority [high|medium|low|all]` (default: all)
  - `--tag <value>` (partial match allowed within tag strings - substring matching)
- Filter logic: AND combination across different filter types (all filters must match)
- Multiple `--tag` flags treated as OR condition (task has one or more of the specified tags)
- Example: `list --status pending --priority high --tag work` → only pending high-priority work tasks
- Example: `list --tag work --tag urgent` → tasks with either 'work' OR 'urgent' tag

### FR-05: Sort Options
- Command flag: `--sort [created|priority|title]`
- Sort behaviors:
  - `created`: Chronological (newest first) — DEFAULT
  - `priority`: High → medium → low (tasks with same priority sorted by creation time, newest first)
  - `title`: Case-insensitive alphabetical A→Z
- Sort applies AFTER filters (sort filtered results only)
- Sort preference NOT persisted between runs (strictly in-memory per session)

### FR-06: Backward Compatibility Guarantees
- All basic commands work WITHOUT intermediate flags:
  - `add "Title" "Desc"` → creates task with medium priority, no tags
  - `list` → shows all tasks with default sort (created)
  - `update 1 "New title" "New desc"` → preserves existing priority/tags
  - No new required parameters for existing commands
  - Existing task IDs remain stable when adding intermediate features

## 3. Acceptance Criteria

### AC-01: Priority Validation
- GIVEN user enters priority "HIGH" (uppercase)
- WHEN task is created
- THEN priority stored as "high" and displayed with `[!]` indicator

### AC-02: Tag Normalization
- GIVEN user enters tags " work , urgent "
- WHEN task is created
- THEN tags stored as ["work", "urgent"] and displayed as `(work, urgent)`

### AC-03: Combined Filters
- GIVEN 5 tasks with mixed statuses/priorities/tags
- WHEN user runs `list --status pending --priority high --tag work`
- THEN ONLY tasks matching ALL three criteria are returned

### AC-04: Search Within Filtered Set
- GIVEN 10 tasks including 3 with "meeting" in title
- WHEN user runs `search "meeting" --status pending`
- THEN ONLY pending tasks containing "meeting" are returned

### AC-05: Sort Stability
- GIVEN 3 high-priority tasks created at different times
- WHEN user runs `list --sort priority`
- THEN tasks sorted high→medium→low, with same-priority tasks sorted newest-first

### AC-06: Zero Breaking Changes
- GIVEN basic-level application state (tasks without priorities/tags)
- WHEN intermediate features are enabled
- THEN all existing tasks remain accessible via original IDs
- AND all basic commands function identically to pre-intermediate behavior

## 4. Domain Model Specification

### Task Entity (Enhanced)
```python
class Task:
    id: int # Stable within session
    title: str # Required, 1-200 chars
    description: str # Optional, max 1000 chars
    completed: bool # Default False
    priority: str # "high" | "medium" | "low" (default "medium")
    tags: list[str] # Empty list when no tags
    created_at: datetime # UTC timestamp
    updated_at: datetime # UTC timestamp
```

Validation Rules:
- Priority: Reject values outside ["high", "medium", "low"] (case-insensitive validation)
- Tags: Split on commas, trim whitespace, discard empty strings
- Title: Required (non-empty after whitespace trim)
- Description: Optional (accepts empty string)

## 5. CLI Command Specification

### add <title> <description> [--priority <level>] [--tag <tags>]
- Priority/tag flags OPTIONAL
- Arguments with spaces must be enclosed in quotes
- Flags can be specified as `--flag value` format
- Example: add "Team sync" "Weekly standup" --priority high --tag work,meeting

### list [--status <filter>] [--priority <filter>] [--tag <value>]... [--sort <option>]
- All flags OPTIONAL with sensible defaults
- Arguments with spaces must be enclosed in quotes
- Flags can be specified as `--flag value` format
- Multiple `--tag` flags allowed (OR condition - task has one or more of the specified tags)
- Example: list --status pending --sort priority
- Example: list --tag work --tag urgent --status pending

### search <keyword> [--status <filter>] [--priority <filter>] [--tag <value>]... [--sort <option>]
- Keyword REQUIRED
- All filter/sort flags OPTIONAL (same as list command)
- Arguments with spaces must be enclosed in quotes
- Flags can be specified as `--flag value` format
- Multiple `--tag` flags allowed (OR condition - task has one or more of the specified tags)
- Example: search "report" --priority high --sort title
- Example: search "meeting" --tag work --tag urgent --status pending

### update <id> <title> <description> [--priority <level>] [--tag <tags>]
- Priority/tag flags OPTIONAL (omitting preserves existing values)
- Arguments with spaces must be enclosed in quotes
- Flags can be specified as `--flag value` format
- Example: update 3 "Updated title" "New desc" --priority low

### delete <id>, complete <id>, view <id>
- NO changes to syntax or behavior from basic level
- Must continue working identically

## Clarifications

### Session 2026-02-08

- Q: How should the CLI parser handle arguments with spaces or special characters? → A: Arguments with spaces must be enclosed in quotes, flags as `--flag value` format
- Q: Should all error messages follow a specific format? → A: All error messages should follow the format "[ERROR] Description"
- Q: Should help be available per command, globally, or both? → A: Help available both per command (e.g., `list --help`) and globally (e.g., `--help`)
- Q: How should tag filtering work with partial match? → A: Partial match means substring matching within tags (e.g., filter "wor" would match tag "work")
- Q: How should multiple `--tag` flags be handled? → A: Multiple `--tag` flags treated as OR condition (task has one or more of the specified tags)

## 6. Edge Cases & Error Handling

### EC-01: Invalid Priority Values
- Input: add "Task" "Desc" --priority critical
- Expected: Clear error message "Invalid priority: 'critical'. Must be high/medium/low"

### EC-02: Empty Tag Strings
- Input: add "Task" "Desc" --tag "" or --tag " "
- Expected: Task created with empty tags list (no error)

### EC-03: Special Characters in Search
- Input: search "C++ project"
- Expected: Literal match for "C++" (no regex interpretation)

### EC-04: Mixed-Case Priority Input
- Input: --priority HIGH or --priority High
- Expected: Normalized to "high" without error

### EC-05: Non-Existent Task IDs in Update
- Input: update 999 "Title" "Desc" --priority high
- Expected: Same error behavior as basic level ("Task 999 not found")

## 7. Non-Functional Requirements

### NFR-01: Performance
- All operations (including filtered/sorted lists) must complete in <100ms with 1000 tasks in memory

### NFR-02: UX Consistency
- Help text (--help) required for all commands with flags
- Help available both per command (e.g., `list --help`) and globally (e.g., `--help`)
- Error messages must be user-friendly and actionable
- All error messages follow the format "[ERROR] Description"
- Empty states must display helpful messages ("No tasks found matching your filters")

### NFR-03: Backward Compatibility
- 100% compatibility with basic-level command syntax and behavior
- Zero regressions in core CRUD operations

### NFR-04: In-Memory Constraint Enforcement
- ZERO file I/O operations permitted (verified via code review)
- ZERO database connections permitted
- All state must reside exclusively in Python objects within the running process