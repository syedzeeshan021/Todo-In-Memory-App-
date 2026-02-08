# Todo In-Memory Python Console App Specification (Advanced Level - Progressive Showcase)

## 1. Progressive User Journey (Single Session Demo Flow)

### Minute 0-20s: Basic CRUD Foundation
- User runs `add "Morning standup" "Team sync"` → task created with default medium priority, no tags
- User runs `list` → sees task with [~] indicator and pending status
- User runs `complete 1` → task marked complete
- Teacher observes: Core functionality works identically to Basic Level

### Minute 20-50s: Intermediate Feature Layering
- User runs `add "Prepare presentation" "Q3 roadmap" --priority high --tag work,urgent`
- User runs `add "Buy groceries" "Milk, eggs" --tag personal`
- User runs `list --priority high --sort title` → sees ONLY high-priority tasks sorted alphabetically
- User runs `search "roadmap" --status pending` → finds presentation task
- Teacher observes: Intermediate features enhance (not replace) basic functionality

### Minute 50-80s: Advanced Feature Integration
- User runs `add "Weekly planning" "Team sync" --recur weekly --due "2026-02-15T09:00:00"`
- User runs `add "Pay rent" "Apartment" --due "2026-02-28T23:59:00" --priority high`
- User completes "Weekly planning" task → system auto-generates next occurrence for next week (same time/day)
- User waits 60 seconds (simulated time passage), then runs ANY command → console displays reminder: `[REMINDER] "Pay rent" due in 20 days!`
- Teacher observes: Advanced features integrate with priorities/tags (high-priority due task) and recurrence works session-bound

### Minute 80-90s: Cross-Feature Synthesis
- User runs `list --status pending --sort due_date` → sees tasks sorted by upcoming deadlines INCLUDING next occurrence of recurring task
- User runs `search "planning" --priority high` → finds recurring high-priority task
- Teacher observes: All three feature levels (Basic + Intermediate + Advanced) working together seamlessly

## 2. Advanced Feature Specifications (Additive to Intermediate)

### AF-01: Recurring Tasks (Session-Bound)
- Supported patterns: `daily`, `weekly`, `monthly` (case-insensitive)
- CLI flag: `--recur <pattern>` (OPTIONAL during add/update)
- Behavior upon completion:
  - When user runs `complete <id>` on recurring task
  - System IMMEDIATELY creates next occurrence with:
    - Same title/description/priority/tags
    - Due date offset by pattern (daily=+1d, weekly=+7d, monthly=+30d)
    - New task ID, `completed=False`
    - Original task marked complete (NOT deleted)
- Critical constraint: Recurrence ONLY works while application remains running (no persistence between sessions)
- Display indicator: `(R:weekly)` suffix after tags in listings

### AF-02: Due Dates & Console Reminders
- Due date format: ISO 8601 (`YYYY-MM-DDTHH:MM:SS`) – parsed via `datetime.fromisoformat()`
- CLI flag: `--due "<iso8601>"` (OPTIONAL during add/update)
- Reminder mechanics:
  - System checks due dates BEFORE displaying ANY command output
  - If current time >= task.due_date AND task.completed=False:
    - Display console alert: `[REMINDER] "<title>" was due <time_ago> ago!` (past due)
    - OR `[REMINDER] "<title>" due in <time_remaining>!` (upcoming within 24h)
  - Reminders trigger on NEXT user interaction after due time passes (no background threads)
  - Display format in listings: `Due: 2026-02-15 09:00` after tags/priority indicators
- Sort option: `--sort due_date` (tasks without due dates appear last)

### AF-03: Cross-Feature Integration Rules
- Recurring + Priority: Next occurrence inherits original priority/tags
- Recurring + Due Date: Next occurrence due date = original due date + pattern offset
- Filter + Due Date: `--due-before <date>` and `--due-after <date>` flags for date-range filtering
- Sort precedence with due_date: Tasks sorted by proximity to current time (soonest first)

## 3. Enhanced Domain Model (Progressive Evolution)

### Task Entity (Final Phase I Form)
```python
class Task:
    id: int # Stable within session
    title: str # Required (Basic)
    description: str # Optional (Basic)
    completed: bool # Default False (Basic)
    priority: str # "high"|"medium"|"low" default "medium" (Intermediate)
    tags: list[str] # Empty list when no tags (Intermediate)
    due_date: datetime | None # None when no due date (Advanced)
    recurrence: str | None # None|"daily"|"weekly"|"monthly" (Advanced)
    created_at: datetime # UTC timestamp (Basic)
    updated_at: datetime # UTC timestamp (Basic)
```

Validation Rules (Progressive)
- Basic: title non-empty
- Intermediate: priority in ["high","medium","low"], tags normalized
- Advanced: due_date must be valid ISO 8601, recurrence in allowed patterns

## 4. Unified CLI Command Specification

### add <title> <description> [flags]
ALL flags OPTIONAL and combinable:
- --priority <level> # Intermediate
- --tag <tags> # Intermediate
- --due <iso8601> # Advanced
- --recur <pattern> # Advanced

Example combining all levels: 
`add "Team sync" "Weekly planning" --priority high --tag work --due "2026-02-15T09:00:00" --recur weekly`

### list [flags]
Extended flags for Advanced features:
- --due-before <date> # Show tasks due before date
- --due-after <date> # Show tasks due after date
- --sort due_date # Sort by upcoming deadlines (Advanced default sort option)

Other commands (update/delete/complete/search)
- update preserves recurrence/due_date unless explicitly overridden
- complete on recurring task triggers next occurrence generation BEFORE returning success message
- search includes due_date fields in keyword matching

## 5. Session-Bound Temporal Constraints (Critical for Phase I)

Explicit Limitations (MUST document in README.md)
- Recurring tasks ONLY generate next occurrences WHILE application remains running
- Due date reminders ONLY trigger during active session (no background monitoring)
- All task state (including recurrence schedules) resets on application restart
- Time simulation for demo: Use --simulate-time "<iso8601>" flag during development ONLY (not for production)

Teacher Evaluation Guidance
This is INTENTIONAL design constraint of Phase I (in-memory only), NOT a bug. Phase II (web app) will add persistence to make recurrence/reminders survive restarts.

## 6. Backward Compatibility Guarantees

Zero Breaking Changes
- Commands without Advanced flags behave IDENTICALLY to Intermediate Level implementation
- Tasks created without due_date/recurrence function identically to Intermediate tasks
- Sort defaults remain created (not due_date) to preserve Intermediate behavior
- All Intermediate acceptance criteria STILL PASS with Advanced features enabled

Feature Detection System automatically detects feature usage:
- Tasks with due_date get reminder checks
- Tasks with recurrence get auto-generation on completion
- Absence of fields = no Advanced behavior triggered

## 7. Acceptance Criteria for Progressive Showcase

### AC-SHOWCASE-01: Single Session Multi-Level Demo
GIVEN fresh application start
WHEN user executes Basic → Intermediate → Advanced commands in sequence WITHOUT restart
THEN all features work correctly AND teacher sees progressive layering in 90-second demo

### AC-SHOWCASE-02: Cross-Feature Filtering
GIVEN task with priority=high, tag=work, due_date=tomorrow, recurrence=weekly
WHEN user runs list --priority high --tag work --due-after today
THEN task appears in results with all metadata displayed correctly

### AC-SHOWCASE-03: Recurrence + Completion Chain
GIVEN recurring weekly task completed at 9:00 AM Monday
WHEN user runs list at 9:01 AM Monday
THEN original task shows as completed AND next occurrence appears with due date next Monday 9:00 AM

### AC-SHOWCASE-04: Reminder Trigger Timing
GIVEN task due at 10:00 AM
WHEN current time is 10:05 AM and user runs ANY command (list, add, etc.)
THEN console displays reminder BEFORE command output

## 8. Repository Structure for Progressive Showcase
```
todo-console/
├── specs/
│   ├── constitution.md # Advanced Level constitution
│   ├── history/
│   │   ├── basic-spec-v1.md
│   │   ├── intermediate-spec-v1.md
│   │   └── advanced-spec-v1.md # THIS SPECIFICATION
│   └── features/
│       ├── basic-crud.md
│       ├── intermediate-features.md
│       └── advanced-features.md # Recurrence + due dates
├── src/
│   ├── core/ # Basic CRUD (unchanged interface)
│   │   ├── models.py # FINAL Task model with all fields
│   │   └── crud.py
│   ├── features/ # Intermediate features
│   │   ├── priorities_tags.py
│   │   └── query.py # Enhanced with due_date filtering/sort
│   └── advanced/ # NEW: Advanced features
│       ├── recurrence.py # Recurrence logic + next occurrence gen
│       └── reminders.py # Due date checks + console alerts
├── tests/
│   ├── test_basic.py # Still pass with Advanced enabled
│   ├── test_intermediate.py # Still pass with Advanced enabled
│   └── test_advanced.py # Recurrence + reminders + integration
├── DEMO_SCRIPT.txt # CRITICAL: 90-second demo command sequence
├── QWEN.md
└── README.md # MUST document session-bound limitations
```

## Clarifications

### Session 2026-02-08

- Q: How should recurrence be calculated when a recurring task is completed? → A: Next occurrence calculated from original due date pattern (e.g., if original was due Monday 9:00 AM, recurrence is due next Monday 9:00 AM regardless of completion time)
- Q: How should the system handle timezone conversion when users specify due dates? → A: All due dates entered by users are converted to UTC for storage and comparison
- Q: How should the system handle tasks created with due dates in the past? → A: Tasks with past due dates are accepted but immediately trigger a reminder when any command is executed
- Q: How should the system handle monthly recurrence when the due date doesn't exist in the following month? → A: Monthly recurrence uses same day of month if possible, otherwise uses the last day of the month (e.g., January 31 → February 28)
- Q: Should reminders for the same overdue task appear only once or on every command execution? → A: Reminders appear once per overdue task until it's completed or due date is modified