# Implementation Tasks: Todo In-Memory Python Console App (Advanced Level)

**Feature**: Todo In-Memory Python Console App with intermediate features (priorities, tags, search, filter, sort)
**Input**: Feature specification from `/specs/3-advanced-features/spec.md`

**Note**: This template is filled in by the `/sp.tasks` command. See `.specify/templates/commands/tasks.md` for the execution workflow.

## Summary

Implementation of advanced features for the Todo In-Memory Python Console App, extending the existing basic and intermediate functionality with recurring tasks and due date reminders while maintaining 100% backward compatibility. The implementation will follow a modular architecture with strict separation of concerns as mandated by the constitution, using only Python standard library components with in-memory storage.

## Dependencies

- User Story 1 (Organizing Tasks with Priorities and Tags) - PRIORITY 1
- User Story 2 (Finding Specific Tasks Efficiently) - PRIORITY 2  
- User Story 3 (Managing Task Visibility Through Sorting) - PRIORITY 3
- User Story 4 (Backward Compatibility Verification) - PRIORITY 4

## Parallel Execution Examples

- US1: Task model enhancement and priority/tag logic can be developed in parallel with CLI parser enhancements
- US2: Search functionality and filter implementation can be developed in parallel after core model changes
- US3: Sort functionality can be developed in parallel with search/filter after core model changes

## Implementation Strategy

- MVP: Implement User Story 1 (Priorities and Tags) with basic recurrence functionality
- Incremental Delivery: Add search/filter functionality (US2), then sorting (US3), then verify backward compatibility (US4)

---

## Phase 1: Setup

- [ ] T001 Create src/features/ directory structure per implementation plan
- [ ] T002 Create src/features/recurrence.py with basic module structure
- [ ] T003 Create src/features/reminders.py with basic module structure
- [ ] T004 Create tests/test_recurrence.py with basic test structure
- [ ] T005 Create tests/test_reminders.py with basic test structure
- [ ] T006 [P] Create __init__.py files in new directories

## Phase 2: Foundational Components

- [ ] T007 Enhance Task model with due_date and recurrence fields in src/core/models.py
- [ ] T008 Update Task validation to include due_date and recurrence constraints in src/core/models.py
- [ ] T009 Implement UTC-only datetime validation in src/features/temporal.py
- [ ] T010 Create ISO 8601 parsing function with UTC enforcement in src/features/temporal.py
- [ ] T011 Add datetime validation tests in tests/test_temporal.py

## Phase 3: [US1] Organizing Tasks with Priorities and Tags

**Goal**: Enable users to add tasks with priorities and tags, and display them appropriately with recurrence capability

**Independent Test Criteria**: 
- User can add a task with priority, tags, and recurrence pattern
- User can list tasks and see priority indicators ([!] for high) and tags displayed
- When completing a recurring task, next occurrence is generated with same properties

**Tasks**:
- [ ] T012 [US1] Implement recurrence pattern calculator in src/features/recurrence.py
- [ ] T013 [US1] Implement next occurrence generator preserving all metadata in src/features/recurrence.py
- [ ] T014 [US1] Add recurrence validation to Task model in src/core/models.py
- [ ] T015 [US1] Update CLI parser to accept --recur flag in src/cli/parser.py
- [ ] T016 [US1] Update add command to handle recurrence option in src/cli/interface.py
- [ ] T017 [US1] Update update command to handle recurrence option in src/cli/interface.py
- [ ] T018 [US1] Add (R:pattern) display indicator to task listings in src/cli/interface.py
- [ ] T019 [US1] Create unit tests for recurrence functionality in tests/test_recurrence.py

## Phase 4: [US2] Finding Specific Tasks Efficiently

**Goal**: Enable users to search and filter tasks by various criteria including due dates

**Independent Test Criteria**:
- User can search tasks by keyword across title/description fields
- User can filter tasks by due date ranges (--due-before, --due-after)
- User can combine multiple filters (status + priority + due date + tags)

**Tasks**:
- [ ] T020 [US2] Implement due date validation and parsing in src/features/reminders.py
- [ ] T021 [US2] Implement reminder check logic in src/features/reminders.py
- [ ] T022 [US2] Update query.py to support due date filtering in src/features/query.py
- [ ] T023 [US2] Add --due-before and --due-after flags to list command in src/cli/parser.py
- [ ] T024 [US2] Add --due-before and --due-after flags to search command in src/cli/parser.py
- [ ] T025 [US2] Update list command to handle due date filters in src/cli/interface.py
- [ ] T026 [US2] Update search command to handle due date filters in src/cli/interface.py
- [ ] T027 [US2] Create unit tests for due date filtering in tests/test_query.py

## Phase 5: [US3] Managing Task Visibility Through Sorting

**Goal**: Enable users to sort task lists by different criteria including due dates

**Independent Test Criteria**:
- User can sort tasks by due date (soonest first, tasks without due dates last)
- User can combine sorting with filtering operations
- Sort applies correctly after filters are applied

**Tasks**:
- [ ] T028 [US3] Implement due date sorting logic in src/features/query.py
- [ ] T029 [US3] Add --sort due_date option to CLI commands in src/cli/parser.py
- [ ] T030 [US3] Update list command to handle due date sorting in src/cli/interface.py
- [ ] T031 [US3] Update search command to handle due date sorting in src/cli/interface.py
- [ ] T032 [US3] Implement proper tie-breaking for due date sorting in src/features/query.py
- [ ] T033 [US3] Create unit tests for due date sorting in tests/test_query.py

## Phase 6: [US4] Reminder System Implementation

**Goal**: Implement console-based reminder system that triggers on user interaction after due time passes

**Independent Test Criteria**:
- User sees reminder message before command output when tasks are overdue
- User sees upcoming due reminders (within 24 hours) before command output
- Reminder system does not interfere with basic functionality

**Tasks**:
- [ ] T034 [US4] Implement console reminder display function in src/features/reminders.py
- [ ] T035 [US4] Integrate reminder check into CLI interface before command output in src/cli/interface.py
- [ ] T036 [US4] Implement reminder formatting with proper past/future tense in src/features/reminders.py
- [ ] T037 [US4] Add reminder tests to verify timing and display in tests/test_reminders.py
- [ ] T038 [US4] Ensure all reminder messages follow "[REMINDER] Description" format in src/features/reminders.py

## Phase 7: Cross-Feature Integration

**Goal**: Ensure all features work together seamlessly with proper interaction handling

**Independent Test Criteria**:
- User can combine recurrence, due dates, priority, and tags in single tasks
- User can filter, sort, and search across all feature dimensions simultaneously
- All existing basic and intermediate functionality continues to work unchanged

**Tasks**:
- [ ] T039 [P] Update complete_task function to trigger recurrence in src/core/crud.py
- [ ] T040 [P] Implement combined filter logic (priority + tags + due dates) in src/features/query.py
- [ ] T041 [P] Update search functionality to include due date fields in src/features/query.py
- [ ] T042 [P] Add integration tests for feature combinations in tests/test_integration.py
- [ ] T043 [P] Verify backward compatibility with all intermediate tests passing in tests/test_integration.py
- [ ] T044 [P] Create end-to-end test for full user journey in tests/test_integration.py

## Phase 8: Polish & Cross-Cutting Concerns

- [X] T045 Update README.md with documentation for new advanced features
- [X] T046 Add demo script for 90-second showcase in DEMO_SCRIPT.txt
- [X] T047 Implement --simulate-time flag for demo purposes in src/cli/parser.py
- [X] T048 Add session-bound limitations documentation to README.md
- [X] T049 Run full test suite to verify all functionality works together
- [X] T050 [P] Add docstrings to all new functions and classes
- [X] T051 Perform final validation of Phase I constraints (in-memory only, CLI only)