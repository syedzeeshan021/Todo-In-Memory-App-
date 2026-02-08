# Implementation Plan: Todo In-Memory Python Console App (Advanced Level)

**Branch**: `3-advanced-features` | **Date**: 2026-02-08 | **Spec**: [link to spec.md](../3-advanced-features/spec.md)
**Input**: Feature specification from `/specs/3-advanced-features/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of advanced features for the Todo In-Memory Python Console App, extending the existing basic and intermediate functionality with recurring tasks and due date reminders while maintaining 100% backward compatibility. The implementation will follow a modular architecture with strict separation of concerns as mandated by the constitution, using only Python standard library components with in-memory storage.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Standard library only (no external dependencies permitted)
**Storage**: In-memory storage using Python data structures (lists/dicts) - NO file I/O or database connections
**Testing**: pytest for unit and integration tests
**Target Platform**: Cross-platform console application
**Project Type**: Single project (console application)
**Performance Goals**: All operations complete in <100ms with 1000 tasks in memory
**Constraints**:
- Strictly in-memory storage (no persistence to files or databases)
- 100% backward compatibility with existing basic and intermediate functionality
- CLI interface only (no GUI/web interface dependencies)
- UV for environment management
- Qwen Code for 100% of implementation and modifications
- Explicit prohibition against background threads/services that imply persistence
**Scale/Scope**: Up to 1000 tasks in memory per session, single-user console application

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Compliance Verification

**I. Spec-Driven Development**: ✅ 
- All features originate from written specification
- Implementation follows spec → plan → tasks sequence

**II. Agentic Workflow**: ✅ 
- Following sequence: spec → clarify → plan → tasks → implement via Qwen Code
- All iterations will be documented in /specs/history/

**III. No Manual Coding**: ✅ 
- All code generation and modifications will happen exclusively through Qwen Code
- No direct manual code editing

**IV. Backward Compatibility**: ✅ 
- All advanced features preserve 100% compatibility with existing basic and intermediate functionality
- Basic commands (add, list, update, delete, complete) will function identically
- No new required fields or breaking changes to existing command syntax

**V. Enhanced Modularity**: ✅ 
- Core CRUD operations remain in /src/core/
- Priority/tag logic resides in /src/features/priorities_tags.py
- Search/filter/sort logic resides in /src/features/query.py
- Recurrence logic resides in /src/features/recurrence.py
- Due date/reminder logic resides in /src/features/reminders.py
- CLI parser routes commands to appropriate modules without tight coupling

**VI. Feature Interaction Safety**: ✅ 
- All combinations of basic, intermediate, and advanced features will be explicitly tested
- Filtering, sorting, and searching will work in combination with recurrence and due dates
- Edge cases with empty tags, mixed-case inputs, and special characters will be handled

### Gate Status: PASSED
All constitutional requirements are satisfied by the planned implementation approach.

## Project Structure

### Documentation (this feature)

```text
specs/3-advanced-features/
├── spec.md              # Feature specification
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
todo-console/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py            # Enhanced Task model with priority/tags/due_date/recurrence fields
│   │   └── crud.py              # Basic CRUD operations (unchanged interface)
│   ├── features/
│   │   ├── __init__.py
│   │   ├── priorities_tags.py   # Priority/tag assignment and validation
│   │   ├── query.py             # Search, filter, and sort logic (enhanced with due_date support)
│   │   ├── recurrence.py        # NEW: Recurrence pattern logic and generation
│   │   └── reminders.py         # NEW: Due date handling and reminder logic
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
│   ├── test_reminders.py        # NEW: Due date and reminder tests
│   └── test_integration.py      # Feature interaction tests
├── QWEN.md                      # Qwen Code usage instructions and project context
├── README.md                    # Setup instructions (UV setup, running app) with temporal limitations documented
└── pyproject.toml               # UV configuration with Python 3.13 constraint
```

**Structure Decision**: Single project console application structure selected, following the architecture specified in the constitution with strict separation of concerns between core CRUD operations, feature-specific logic, and CLI interface.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitutional violations identified. All requirements from the constitution are satisfied by the planned implementation approach.

## Phase 0: Research & Clarification

### Research Summary

The following technical decisions have been researched and clarified based on the specification and constraints:

1. **Datetime Handling**: Using Python's built-in `datetime.fromisoformat()` for ISO 8601 parsing with UTC enforcement
2. **Recurrence Calculation**: Fixed interval approach (daily=+1 day, weekly=+7 days, monthly=+30 days) for simplicity within standard library constraints
3. **Reminder Mechanics**: Triggered on next user interaction after due time passes, not background monitoring
4. **CLI Argument Parsing**: Using argparse with optional flags for advanced features while preserving all basic functionality
5. **Memory Storage**: Using Python lists/dicts for in-memory storage with session-bound persistence only

### Key Decisions Made

- **Monthly Recurrence**: Using fixed 30-day intervals rather than calendar-aware months to maintain simplicity
- **Reminder Frequency**: Reminders appear on every command execution after due time passes (rather than once-only)
- **Timezone Handling**: All datetimes stored in UTC to avoid timezone complications
- **Recurrence Termination**: No mechanism to disable recurrence after creation (must delete and recreate)

## Phase 1: Design & Architecture

### Data Model Design

The enhanced Task entity will include all fields from basic and intermediate levels, plus new fields for advanced features:

```python
class Task:
    id: int  # Stable within session
    title: str  # Required (Basic)
    description: str  # Optional (Basic)
    completed: bool  # Default False (Basic)
    priority: str  # "high"|"medium"|"low" default "medium" (Intermediate)
    tags: list[str]  # Empty list when no tags (Intermediate)
    due_date: datetime | None  # None when no due date (Advanced)
    recurrence: str | None  # None|"daily"|"weekly"|"monthly" (Advanced)
    created_at: datetime  # UTC timestamp (Basic)
    updated_at: datetime  # UTC timestamp (Basic)
```

### API Contracts

The CLI interface will be extended with new optional flags while preserving all existing functionality:

- `add` command: `--due "<iso8601>"` and `--recur "<pattern>"` flags
- `list` command: `--due-before`, `--due-after`, and `--sort due_date` flags
- `search` command: Will include due dates in keyword matching
- `complete` command: Will trigger next occurrence generation for recurring tasks

### Quickstart Guide

The implementation will follow these phases:

1. **Foundation**: Set up project structure and enhanced Task model
2. **Core Advanced Features**: Implement recurrence and reminder logic
3. **CLI Integration**: Add advanced flags to existing commands
4. **Integration & Testing**: Ensure all features work together and maintain backward compatibility

## Phase 2: Implementation Plan

### Implementation Phases

**Phase A: Temporal Foundation**
- Implement UTC datetime handling utilities
- Create temporal.py module with ISO 8601 parsing/validation
- Unit tests for datetime edge cases

**Phase B: Due Date Integration** 
- Enhance Task model with due_date field
- Implement reminder checking logic
- Add due date CLI flags

**Phase C: Recurrence Engine**
- Implement recurrence pattern logic
- Create next occurrence generation
- Add recurrence CLI flags

**Phase D: Integration & Validation**
- Connect all components
- Ensure backward compatibility
- Create comprehensive tests
- Validate 90-second demo flow

## Risk Assessment

### High-Risk Areas

1. **Datetime Handling**: Potential for timezone-related bugs - mitigated by enforcing UTC-only storage
2. **Memory Usage**: Large number of tasks could impact performance - mitigated by in-memory efficiency with standard library
3. **CLI Complexity**: Many optional flags could make interface confusing - mitigated by preserving simple usage patterns

### Mitigation Strategies

- Extensive unit testing for datetime operations
- Performance testing with 1000+ tasks
- Clear help text and documentation for CLI flags
- Comprehensive integration tests to ensure backward compatibility

## Dependencies

- User Story 1 (Organizing Tasks with Priorities and Tags) - PRIORITY 1
- User Story 2 (Finding Specific Tasks Efficiently) - PRIORITY 2  
- User Story 3 (Managing Task Visibility Through Sorting) - PRIORITY 3
- User Story 4 (Backward Compatibility Verification) - PRIORITY 4

## Parallel Execution Examples

- Phase A (Temporal Foundation) can be developed in parallel with Phase B (Due Date Integration)
- Phase C (Recurrence Engine) can be developed in parallel with Phase B after foundation is complete
- Testing can be developed alongside implementation

## Implementation Strategy

- MVP: Implement User Story 1 (Priorities and Tags) with basic recurrence functionality
- Incremental Delivery: Add due date reminders (US2), then advanced filtering/sorting (US3), then verify backward compatibility (US4)