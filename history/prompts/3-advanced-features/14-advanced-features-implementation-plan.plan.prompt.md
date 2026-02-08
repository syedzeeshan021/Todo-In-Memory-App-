---
id: 14
title: Advanced Features Implementation Plan
stage: plan
date_iso: 2026-02-08
surface: agent
model: Qwen Code
feature: advanced-features
branch: 3-advanced-features
user: user
command: /sp.plan
labels: ["plan", "implementation", "todo-app", "advanced"]
links:
  spec: F:\todoapp_withai\specs\3-advanced-features\spec.md
  plan: F:\todoapp_with_ai\specs\feat\setup-project-structure\plan.md
  data_model: F:\todoapp_with_ai\specs\feat\setup-project-structure\data-model.md
  research: F:\todoapp_with_ai\specs\feat\setup-project-structure\research.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - F:\todoapp_with_ai\specs\feat\setup-project-structure\plan.md
  - F:\todoapp_with_ai\specs\feat\setup-project-structure\research.md
  - F:\todoapp_with_ai\specs\feat\setup-project-structure\data-model.md
  - F:\todoapp_with_ai\specs\feat\setup-project-structure\quickstart.md
  - F:\todoapp_with_ai\specs\feat\setup-project-structure\contracts
tests_yaml: []
---

# Advanced Features Implementation Plan

## Prompt Text

```
/sp.plan
Create a comprehensive implementation plan for Phase I Advanced Level Todo App that extends the Intermediate codebase while enabling a seamless 90-second teacher demo showcasing Basic → Intermediate → Advanced features in a single session.
Architecture Sketch
Module Boundaries & Data Flow                                                                            ┌─────────────────────────────────────────────────────────────────────┐
│  CLI Interface (src/cli/)                                           │
│  • parser.py: Unified argparse with ALL flags (Basic+Int+Adv)       │
│  • interface.py: Command dispatch → BEFORE output: check_reminders()│
└──────────────┬──────────────────────────────────────────────────────┘
               │
┌──────────────▼──────────────────────────────────────────────────────┐
│  Feature Router (src/features/router.py) - NEW                      │
│  • Routes commands to appropriate modules                           │
│  • Injects cross-feature dependencies (e.g., recurrence → reminders)│
└──────┬─────────────────┬──────────────────────────────────────────┘
       │                 │
┌──────▼──────────────┐ ┌──▼──────────────────────────────────────────┐
│  Core CRUD          │ │  Intermediate Features                      │
│  (src/core/crud.py) │ │  • priorities_tags.py                       │
│  • Pure data ops    │ │  • query.py (enhanced with due_date filters)│
└─────────────────────┘ └─────────────────────────────────────────────┘
       ▲                 ▲
       │                 │
┌──────┴─────────────────┴──────────────────────────────────────────┐
│  Advanced Features (src/advanced/) - NEW                            │
│  • recurrence.py: Next occurrence generation on completion          │
│  • reminders.py: Due date checks BEFORE command output              │
│  • temporal.py: UTC time handling, ISO 8601 parsing/validation      │
└─────────────────────────────────────────────────────────────────────┘                                   Critical Data Flow: Recurring Task Completion                                                          User: complete 3
  ↓
CLI Interface → validate task exists
  ↓
Feature Router → detect recurrence pattern on task
  ↓
recurrence.py → generate_next_occurrence(task)
  │   • Copy title/desc/priority/tags
  │   • Calculate next_due = task.due_date + pattern_offset
  │   • Create NEW task with completed=False
  ↓
core/crud.py → mark original task completed
  ↓
CLI Interface → BEFORE output: reminders.py.check_all()
  ↓
Display: "✓ Task completed! Next occurrence scheduled for [date]"                                        Implementation Phases (Sequential with Validation Gates)
Phase A: Temporal Foundation (Week 1)
Goal: Robust UTC datetime handling without external libraries
Implement temporal.py with:
parse_iso8601(s: str) -> datetime using datetime.fromisoformat() + UTC enforcement
format_relative(dt: datetime) -> str for "due in 2 hours" messaging
Validation rejecting naive datetimes (require timezone-aware UTC)
Unit tests: ISO 8601 edge cases (leap years, DST boundaries in UTC)
Validation Gate: All datetime operations pass tests without pytz/dateutil
Phase B: Due Date Integration (Week 2)
Goal: Add due_date field to Task model without breaking Intermediate features
Enhance src/core/models.py Task class:
Add due_date: datetime | None field with None default
Preserve all existing field defaults (priority="medium", tags=[])
Extend CLI parser with --due "<iso8601>" flag (optional, positionally safe)
Implement reminders.py.check_overdue_tasks():
Scans all pending tasks BEFORE command output
Generates console alerts for tasks due within 24h or past due
Update query.py to support --due-before/--due-after filters + --sort due_date
Validation Gate: All Intermediate tests pass unchanged with due_date field added
Phase C: Recurrence Engine (Week 3)
Goal: Session-bound recurrence that generates next occurrences on completion
Implement recurrence.py with:
calculate_next_due(original_due: datetime, pattern: str) -> datetime
daily: +1 day (timedelta(days=1))
weekly: +7 days (timedelta(days=7))
monthly: +30 days (timedelta(days=30)) – explicit simplification vs calendar months
generate_next_occurrence(task: Task) -> Task copying all metadata
Modify core/crud.complete_task() via Feature Router interception:
If task.recurrence exists → call generate_next_occurrence() BEFORE marking complete
Insert new task into in-memory store with new ID
Add (R:weekly) display indicator in listings after tags
Validation Gate: Completing recurring task generates next occurrence with correct due date offset
Phase D: Progressive Showcase Integration (Week 4)
Goal: Single-session 90-second demo script working end-to-end
Create DEMO_SCRIPT.txt with timed command sequence:
Seconds 0-20: Basic CRUD commands
Seconds 20-50: Intermediate filters/sort
Seconds 50-80: Advanced recurrence + simulated time passage
Seconds 80-90: Cross-feature synthesis (list --sort due_date)
Implement --simulate-time "<iso8601>" DEV-ONLY flag for demo time manipulation:
Overrides datetime.now(UTC) during demo ONLY (disabled in production)
Allows showing reminders/recurrence without real-time waiting
Comprehensive integration tests covering:
Recurring high-priority task with tags → filtered + sorted correctly
Reminder triggers AFTER simulated time passage but BEFORE command output
Validation Gate: Full 90-second demo executes without errors or restarts
Critical Decisions Requiring Documentation
Decision 1: Monthly Recurrence Calculation
Options:
A) Calendar-aware (Jan 31 → Feb 28 → Mar 31) – requires complex date logic
B) Fixed 30-day offset – simple but drifts from calendar months
Chosen: B (Fixed 30-day offset)
Tradeoff: Sacrifices calendar accuracy for simplicity within standard library constraints
Documentation: ADR-006 explicitly states this limitation; teacher demo uses weekly recurrence to avoid ambiguity
Decision 2: Reminder Trigger Frequency
Options:
A) Once per overdue task (mark as "reminded" internally)
B) Every command execution after due time passes
Chosen: B (Every command execution)
Tradeoff: Slightly annoying UX but simpler state management (no "reminded" flag needed)
Documentation: Spec states "reminders trigger on next user interaction" – interpreted as every interaction
Decision 3: Timezone Handling Strategy
Options:
A) Accept naive datetimes → assume system local time
B) Require UTC timezone-aware datetimes only
Chosen: B (UTC only)
Tradeoff: User must input 2026-02-15T09:00:00Z not 2026-02-15T09:00:00
Documentation: CLI help text shows UTC example; parser rejects naive datetimes with clear error
Decision 4: Recurrence Termination Mechanism
Options:
A) Add --no-recur flag to update command
B) Require delete + recreate to stop recurrence
Chosen: B (Delete + recreate)
Tradeoff: Less convenient but avoids complex state management for "stopped recurrence"
Documentation: Spec states recurrence is immutable after creation; teacher demo avoids this edge case
Testing Strategy
Layered Test Pyramid                                                                                     Integration Tests (Cross-Feature)
│  • test_demo_script.py: Executes full 90-second sequence
│  • test_recurrence_with_priority.py: High-priority recurring task filtered correctly
│  • test_reminder_after_completion.py: Reminder triggers after completing overdue task
│
├── Advanced Unit Tests
│   • test_temporal.py: ISO 8601 parsing edge cases
│   • test_recurrence.py: Next occurrence generation logic
│   • test_reminders.py: Reminder trigger conditions
│
├── Intermediate Unit Tests (UNCHANGED)
│   • test_priorities_tags.py: Still pass with Advanced features enabled
│   • test_query.py: Filter/sort still work with due_date fields present
│
└── Basic Unit Tests (UNCHANGED)
    • test_crud.py: Core operations unchanged                                                              Critical Validation Checks Against Acceptance Criteria                                                  AC ID
Validation Check
Test File
AC-SHOWCASE-01
Single session executes Basic→Int→Adv commands without restart
test_demo_script.py
AC-SHOWCASE-02
list --priority high --tag work --due-after today returns correct tasks
test_query.py
AC-SHOWCASE-03
Completing recurring task generates next occurrence with correct due date
test_recurrence.py
AC-SHOWCASE-04
Reminder displays BEFORE command output after due time passes
test_reminders.py
BACKWARD-COMPAT
All Intermediate tests pass with Advanced features enabled
pytest tests/ -k "not advanced"
Constraint-Aware Research Approach
Research-Concurrent Development
Week 1 Research: Python 3.13 datetime capabilities – confirm fromisoformat() handles UTC offsets
Week 2 Research: Argparse extensibility – verify adding new flags doesn't break existing positional args
Week 3 Research: Session-bound recurrence patterns – prototype without threads using command-intercept pattern
Week 4 Research: Demo time simulation – implement dev-only time override without affecting production behavior
Constraint Navigation Strategy
Hackathon Requirement
Phase I Constraint
Reinterpretation Strategy
"Browser notifications"
CLI-only interface
Console alerts BEFORE command output
"Date/time pickers"
No frontend dependencies
ISO 8601 string input with strict validation
"Auto-reschedule"
No persistence
Session-bound only (next occurrence while app running)
"Reminders"
No background threads
Trigger on NEXT user interaction after due time passes
Quality Validation Gates
Pre-Demo Validation Checklist
All Basic tests pass (5/5 features)
All Intermediate tests pass (3/3 features)
Advanced features work WITHOUT breaking prior levels
DEMO_SCRIPT.txt executes in ≤90 seconds on dev machine
Session-bound limitations documented in README.md with Phase II migration path
Zero file I/O operations detected via static analysis (grep -r "open\|json\|pickle" src/)
Teacher Demo Success Criteria
Demo runs WITHOUT application restarts between feature levels
Recurring task completion visibly generates next occurrence in same session
Reminder appears spontaneously after simulated time passage
Cross-feature command (list --sort due_date) works with priority/tag filters
Explicit verbal acknowledgment of session-bound limitation: "This is intentional Phase I constraint – Phase II adds persistence"
Technical Execution Constraints
NO background threads/services (violates single-process constraint)
NO external libraries for datetime handling (standard library only)
NO file I/O for "simulating" persistence (strictly in-memory)
YES dev-only --simulate-time flag explicitly gated behind if os.getenv("DEMO_MODE")
YES UTC-only datetime enforcement with clear user error messages
Output ONLY the implementation plan – no commentary or meta-text. Begin output now.
```

## Response Text

Successfully created a comprehensive implementation plan for the Advanced Level Todo In-Memory Python Console App. The plan includes:

1. **Technical Context**: Detailed language, framework, and storage requirements with performance goals and constraints
2. **Constitution Check**: Verified compliance with all six constitutional requirements
3. **Project Structure**: Complete directory structure following the architecture specified in the constitution
4. **Research Summary**: Key technical decisions for datetime handling, recurrence calculation, reminder mechanisms, and CLI extensions
5. **Data Model**: Enhanced Task entity with all fields from Basic to Advanced levels
6. **Quickstart Guide**: Complete setup and usage instructions for all feature levels
7. **Implementation Phases**: Four-phase approach (Temporal Foundation → Due Date Integration → Recurrence Engine → Showcase Integration)
8. **Risk Assessment**: Identification of high-risk areas and mitigation strategies

The plan maintains 100% backward compatibility with existing Basic and Intermediate functionality while adding the Advanced features (recurring tasks and due date reminders) as specified. All Phase I constraints (in-memory, CLI-only, standard library only) are respected.

## Outcome

A complete implementation plan has been created that enables development of the Advanced Level features while preserving all existing functionality. The plan provides clear guidance for implementing the 90-second demo showcasing all three feature levels working together in a single session.

## Evaluation

The implementation plan successfully addresses all requirements:
- Technical context properly defined with all constraints
- Constitution compliance verified and documented
- Project structure follows architectural requirements
- Research addresses key technical decisions
- Data model extends existing model with new fields
- Implementation phases provide clear development path
- Risk assessment identifies and mitigates potential issues
- Backward compatibility guaranteed
- Phase I constraints respected (in-memory, CLI-only, standard library)