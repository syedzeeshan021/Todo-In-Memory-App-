<!-- SYNC IMPACT REPORT
Version change: 1.1.0 → 1.2.0
Modified principles: None (new constitution)
Added sections: Core Principles VII-IX, Rules and Regulations, Technical Constraints, Repository Structure, Governance for Advanced Level
Removed sections: None
Templates requiring updates: ⚠ pending (.specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md)
Follow-up TODOs: None
-->

# Todo In-Memory Python Console App Constitution (Advanced Level)

## Core Principles

### I. Spec-Driven Development
All features must originate from a written specification. No implementation without a spec, plan, and tasks. This ensures clear requirements, testable outcomes, and prevents scope creep during development. Advanced features must be specified before any modification to existing code.

### II. Agentic Workflow
Follow the sequence strictly: Write spec → Clarify ambiguities → Generate plan → Break into tasks → Implement via AI tools (Qwen Code). Iterations must be documented in /specs/history/. This maintains discipline when extending the existing codebase with advanced functionality.

### III. No Manual Coding
Developers (human or AI) must not write code directly. All code generation and modifications happen exclusively through Qwen Code. Refine specifications until Qwen Code produces correct output—never bypass the spec-driven loop or manually edit generated code.

### IV. Backward Compatibility
All advanced features must preserve 100% compatibility with existing basic and intermediate functionality. Users must be able to:
- Execute all basic commands (add, list, update, delete, complete) without encountering new required fields
- Use the application without engaging intermediate or advanced features
- Experience zero breaking changes to existing command syntax or behavior

### V. Enhanced Modularity
Advanced features must be implemented with strict separation of concerns:
- Core CRUD operations remain in /src/core/
- Priority/tag logic resides in /src/features/priorities_tags.py
- Search/filter/sort logic resides in /src/features/query.py
- Recurrence logic resides in /src/features/recurrence.py
- Due date/reminder logic resides in /src/features/due_dates.py
- CLI parser must route commands to appropriate modules without tight coupling

### VI. Feature Interaction Safety
All combinations of basic, intermediate, and advanced features must be explicitly tested and specified:
- Filtering completed high-priority tasks with specific tags
- Sorting filtered results by multiple criteria
- Searching within filtered subsets
- Recurring tasks with priorities, tags, and filters
- Due date interactions with all other features
- Edge cases involving empty tags, mixed-case inputs, and special characters

### VII. Session-Bound Recurrence Integrity
Recurring tasks must maintain integrity within the current session only:
- Recurrence patterns (daily/weekly/monthly) generate next occurrence only upon completion within the same running session
- When application exits, recurring tasks do not persist to next session
- Recurrence state is held in-memory only and resets on application restart
- All recurrence logic must be deterministic and reproducible within session bounds

### VIII. Console-First Reminder Design
All reminder functionality must be implemented through console interface only:
- Due date reminders appear as console alerts during user interactions
- Reminders are triggered based on system time comparison during command execution
- No background processes or threads for reminder delivery
- Reminders are displayed as console messages when due time is reached or passed

### IX. Temporal Data Safety
All date/time operations must follow strict safety protocols:
- Use ISO 8601 format exclusively for date/time input and storage
- Store all datetime values in UTC to avoid timezone complications
- Validate date/time inputs for validity and reasonableness
- Prevent creation of invalid or impossible date/time combinations

## Rules and Regulations

### Required Advanced Features (In-Memory Implementation)

#### Recurring Tasks
- Session-bound recurrence patterns (daily/weekly/monthly) that auto-generate next occurrence upon completion within the same running session only
- Daily recurrence: Creates new task with same properties the next day when completed
- Weekly recurrence: Creates new task with same properties the next week when completed
- Monthly recurrence: Creates new task with same properties the next month when completed
- Recurrence only generates next occurrence while app remains running
- Recurrence state is reset when application exits

#### Due Dates & Reminders
- ISO 8601 datetime support (e.g., "2026-12-31T23:59:59" or "2026-12-31")
- Console-based reminder alerts that print on next user interaction after due time passes
- Due date format: Full ISO 8601 datetime or date-only format
- Reminder mechanics: Check for overdue tasks on each command execution
- Due dates persist with tasks through completion and recurrence

#### Recurrence + Due Date Interactions
- Next occurrence inherits due date offset from original (e.g., if original was due tomorrow, recurrence is due tomorrow relative to creation)
- Completed recurring task with due date generates new instance with adjusted due date
- Due date modifications apply only to current instance, not future recurrences

### Technical Constraints

#### Storage
- Strictly in-memory storage using Python data structures (lists/dicts)
- Explicit prohibition: No file I/O, no database connections, no environment variables for persistence
- Task IDs must remain stable within session but reset on application restart
- All state must reside in Python objects within the running process
- Explicit prohibition against background threads/services that imply persistence

#### CLI Interface
- Preserve all basic command syntax unchanged:
  - add "Title" "Description"
  - list
  - complete 3
  - delete 2
  - update 1 "New Title" "New Desc"
- Add optional flags to commands to support advanced features:
  - Add `--due <datetime>` flag to add command for due dates
  - Add `--recur <pattern>` flag to add command for recurrence (pattern: daily, weekly, monthly)
  - All advanced flags must be optional; commands work without flags
  - Flag syntax: --flag value or --flag=value
  - Implement search <keyword> command with same filter/sort flags as list
- User experience must remain intuitive; help text (--help) required for all commands
- CLI interface rules: preserve all prior command syntax while adding optional `--due` and `--recur` flags

#### Technology Stack
- UV for environment management and dependency isolation
- Python 3.13+ exclusively
- Qwen Code for 100% of implementation and modifications
- Spec-Kit Plus for specification management
- Standard library only—no external dependencies permitted (including dateutil, croniter)
- Explicit prohibition: NO browser APIs, NO system notifications, NO background daemons

## Testing Requirements

### Unit Tests
- Test all advanced features in isolation:
  - Recurrence pattern logic and generation
  - Due date parsing and validation
  - Reminder trigger mechanics
  - Session-bound recurrence behavior
- Test feature interactions:
  - Recurring tasks with priorities and tags
  - Due dates with filters and search
  - Recurrence with sort operations
- Edge case coverage:
  - Invalid ISO 8601 date formats
  - Past due dates
  - Recurrence patterns with due dates
  - App exit before recurrence triggers

### Integration Tests
- Demonstrate complete user workflows:
  - Add recurring task with due date → Complete task → Verify next occurrence generated
  - Add task with due date → Wait for time to pass → Verify reminder appears
  - Chain recurrence, due dates, priorities, tags, and filters in single workflow
- Verify backward compatibility:
  - Basic commands function identically to pre-advanced implementation
  - Intermediate commands function identically with advanced features
  - No regression in core CRUD operations

### Temporal Boundary Tests
- Test due dates in past/future
- Test timezone handling via UTC only
- Test recurrence timing accuracy
- Test session-bound behavior (app exit/restart scenarios)

## Repository Structure
```
todo-console/
├── .spec-kit/
│   └── config.yaml
├── specs/
│   ├── constitution.md          # THIS FILE
│   ├── history/                 # All spec iterations with timestamps
│   ├── features/
│   │   ├── basic-crud.md        # Basic functionality spec (unchanged)
│   │   ├── intermediate-features.md  # Intermediate features spec (unchanged)
│   │   └── advanced-features.md  # NEW: Detailed spec for recurrence, due dates, reminders
│   └── architecture/
│       └── in-memory-design.md  # Updated with advanced feature integration
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py            # Enhanced Task model with recurrence/due date fields
│   │   └── crud.py              # Basic CRUD operations (unchanged interface)
│   ├── features/
│   │   ├── __init__.py
│   │   ├── priorities_tags.py   # Priority/tag assignment and validation
│   │   ├── query.py             # Search, filter, and sort logic
│   │   ├── recurrence.py        # NEW: Recurrence pattern logic and generation
│   │   └── due_dates.py         # NEW: Due date handling and reminder logic
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── parser.py            # Enhanced argument parser with advanced flags
│   │   └── interface.py         # Command dispatch and output formatting
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py             # Basic CRUD tests (unchanged)
│   ├── test_priorities_tags.py  # Priority/tag logic tests
│   ├── test_query.py            # Search/filter/sort tests
│   ├── test_recurrence.py       # NEW: Recurrence logic tests
│   ├── test_due_dates.py        # NEW: Due date and reminder tests
│   └── test_integration.py      # Feature interaction tests
├── QWEN.md                      # Qwen Code usage instructions and project context
├── README.md                    # Setup instructions (UV setup, running app) with temporal limitations documented
└── pyproject.toml               # UV configuration with Python 3.13 constraint
```

## Governance
This constitution governs the extension of Phase I (In-Memory Console App) with advanced features while maintaining strict adherence to spec-driven development principles. All implementations must:
- Preserve 100% backward compatibility—basic and intermediate commands must function identically to the completed basic/intermediate-level implementations
- Follow the agentic workflow without manual coding exceptions—Qwen Code must generate 100% of new and modified code
- Document all specification iterations in /specs/history/ with timestamps and change rationales
- Demonstrate all advanced features and their interactions in the 90-second demo video
- Declare session-bound nature of Advanced features as intentional design constraint (not a bug)
- Require explicit documentation of temporal limitations in README.md

Critical Enforcement Rules:
- Any implementation that breaks basic or intermediate functionality invalidates the entire advanced phase
- Any manual code edits (outside Qwen Code generation) invalidate the submission
- Any persistence mechanism (file/database) violates the in-memory constraint and invalidates the phase
- Any browser APIs, system notifications, or background daemons violate the CLI-only constraint
- All feature interactions must be explicitly specified before implementation—no emergent behavior allowed

Amendments to this constitution require explicit documentation in /specs/history/ with justification tied to user experience constraints or technical infeasibility.

**Version**: 1.2.0 | **Ratified**: TODO(RATIFICATION_DATE): Date of original adoption | **Last Amended**: 2026-02-08