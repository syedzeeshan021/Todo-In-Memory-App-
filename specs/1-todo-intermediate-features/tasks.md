# Implementation Tasks: Todo In-Memory Python Console App (Intermediate Level)

**Feature**: Todo In-Memory Python Console App with intermediate features (priorities, tags, search, filter, sort)
**Input**: Feature specification from `/specs/1-todo-intermediate-features/spec.md`

**Note**: This template is filled in by the `/sp.tasks` command. See `.specify/templates/commands/tasks.md` for the execution workflow.

## Summary

Implementation of intermediate features for the Todo In-Memory Python Console App, extending the existing basic CRUD functionality with priorities, tags, search, filter, and sort capabilities while maintaining 100% backward compatibility. The implementation will follow a modular architecture with strict separation of concerns as mandated by the constitution, using only Python standard library components with in-memory storage.

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

- MVP: Implement User Story 1 (Priorities and Tags) with basic functionality
- Incremental Delivery: Add search/filter functionality (US2), then sorting (US3), then verify backward compatibility (US4)

---

## Phase 1: Setup

- [X] T001 Create project directory structure per implementation plan
- [X] T002 Initialize pyproject.toml with Python 3.13+ requirement and UV configuration
- [X] T003 Create initial README.md with setup instructions
- [X] T004 Create src/ directory structure (core/, features/, cli/)
- [X] T005 Create tests/ directory structure (test_core.py, test_priorities_tags.py, test_query.py, test_integration.py)
- [X] T006 [P] Create __init__.py files in all directories

## Phase 2: Foundational Components

- [X] T007 Implement basic Task model in src/core/models.py with enhanced fields (priority, tags)
- [X] T008 Implement TaskManager class in src/core/crud.py with in-memory storage
- [X] T009 Implement basic CLI argument parser in src/cli/parser.py using argparse
- [X] T010 [P] Create interface module in src/cli/interface.py for command dispatch
- [X] T011 [P] Create features/__init__.py and core/__init__.py files

## Phase 3: [US1] Organizing Tasks with Priorities and Tags

**Goal**: Enable users to add tasks with priorities and tags, and display them appropriately

**Independent Test Criteria**: 
- User can add a task with priority and tags
- User can list tasks and see priority indicators and tags
- User can filter tasks by priority and tags

**Tasks**:
- [X] T012 [US1] Enhance Task model validation for priority field in src/core/models.py
- [X] T013 [US1] Enhance Task model validation for tags field in src/core/models.py
- [X] T014 [US1] Implement priority normalization (case-insensitive) in src/core/models.py
- [X] T015 [US1] Implement tag parsing (comma-separated to list) in src/core/models.py
- [X] T016 [US1] Update create_task method to accept priority and tags in src/core/crud.py
- [X] T017 [US1] Update update_task method to handle priority and tags in src/core/crud.py
- [X] T018 [US1] Add --priority and --tag options to add command in src/cli/parser.py
- [X] T019 [US1] Add --priority and --tag options to update command in src/cli/parser.py
- [X] T020 [US1] Implement priority display indicators ([!], [~], [ ]) in src/cli/interface.py
- [X] T021 [US1] Implement tag display format in parentheses in src/cli/interface.py
- [X] T022 [US1] Add priority and tag handling to add command execution in src/cli/interface.py
- [X] T023 [US1] Add priority and tag handling to update command execution in src/cli/interface.py
- [X] T024 [US1] Create unit tests for priority and tag functionality in tests/test_priorities_tags.py

## Phase 4: [US2] Finding Specific Tasks Efficiently

**Goal**: Enable users to search and filter tasks by various criteria

**Independent Test Criteria**:
- User can search tasks by keyword in title/description
- User can filter tasks by status, priority, and tags
- User can combine multiple filters

**Tasks**:
- [X] T025 [US2] Implement search functionality in src/features/query.py
- [X] T026 [US2] Implement filter by status functionality in src/features/query.py
- [X] T027 [US2] Implement filter by priority functionality in src/features/query.py
- [X] T028 [US2] Implement filter by tag functionality in src/features/query.py
- [X] T029 [US2] Implement combined filter logic (AND combination) in src/features/query.py
- [X] T030 [US2] Add search command to CLI parser in src/cli/parser.py
- [X] T031 [US2] Add filter options to list command in src/cli/parser.py
- [X] T032 [US2] Add filter options to search command in src/cli/parser.py
- [X] T033 [US2] Implement search command execution in src/cli/interface.py
- [X] T034 [US2] Update list command to handle filters in src/cli/interface.py
- [X] T035 [US2] Implement tag matching logic (substring matching) in src/features/query.py
- [X] T036 [US2] Add multiple --tag flag handling (OR condition) in src/features/query.py
- [X] T037 [US2] Create unit tests for search and filter functionality in tests/test_query.py

## Phase 5: [US3] Managing Task Visibility Through Sorting

**Goal**: Enable users to sort task lists by different criteria

**Independent Test Criteria**:
- User can sort tasks by creation date
- User can sort tasks by priority (high → medium → low)
- User can sort tasks by title (alphabetical)
- Sort applies after filters are applied

**Tasks**:
- [X] T038 [US3] Implement sort by creation date in src/features/query.py
- [X] T039 [US3] Implement sort by priority (high → medium → low) in src/features/query.py
- [X] T040 [US3] Implement sort by title (alphabetical) in src/features/query.py
- [X] T041 [US3] Implement tie-breaking rules for priority sort in src/features/query.py
- [X] T042 [US3] Add --sort option to list command in src/cli/parser.py
- [X] T043 [US3] Add --sort option to search command in src/cli/parser.py
- [X] T044 [US3] Implement sort handling in list command execution in src/cli/interface.py
- [X] T045 [US3] Implement sort handling in search command execution in src/cli/interface.py
- [X] T046 [US3] Ensure sort applies after filters in src/features/query.py
- [X] T047 [US3] Create unit tests for sorting functionality in tests/test_query.py

## Phase 6: [US4] Backward Compatibility Verification

**Goal**: Ensure all basic commands work identically to basic-level implementation

**Independent Test Criteria**:
- Basic commands (add, list, update, delete, complete) function identically
- No new required fields or breaking changes to existing syntax
- Existing task IDs remain stable

**Tasks**:
- [X] T048 [US4] Verify add command works without priority/tag flags in src/cli/interface.py
- [X] T049 [US4] Verify list command works without filter/sort flags in src/cli/interface.py
- [X] T050 [US4] Verify update command works without priority/tag flags in src/cli/interface.py
- [X] T051 [US4] Verify all basic CRUD operations maintain original behavior in src/core/crud.py
- [X] T052 [US4] Update default values to maintain backward compatibility in src/core/models.py
- [X] T053 [US4] Create integration tests to verify backward compatibility in tests/test_integration.py
- [X] T054 [US4] Test that existing basic commands function identically in tests/test_core.py

## Phase 7: Polish & Cross-Cutting Concerns

- [X] T055 Implement consistent error message format "[ERROR] Description" across all modules
- [X] T056 Add help text for all commands with flags in src/cli/parser.py
- [X] T057 Implement empty state messages for filtered/search results in src/cli/interface.py
- [X] T058 Add performance validation (<100ms with 1000 tasks) in src/features/query.py
- [X] T059 Create comprehensive integration tests in tests/test_integration.py
- [X] T060 Update README.md with usage instructions for new features
- [X] T061 [P] Add docstrings to all public methods and classes
- [X] T062 Run full test suite to verify all functionality works together