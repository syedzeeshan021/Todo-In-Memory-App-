---
id: 16
title: Advanced Features Tasks Generation
stage: tasks
date_iso: 2026-02-08
surface: agent
model: Qwen Code
feature: todo-advanced-features
branch: 3-advanced-features
user: user
command: /sp.tasks
labels: ["tasks", "implementation", "todo-app", "advanced"]
links:
  spec: F:\todoapp_withai\specs\3-advanced-features\spec.md
  plan: F:\todoapp_withai\specs\feat\setup-project-structure\plan.md
  data_model: F:\todoapp_withai\specs\feat\setup-project-structure\data-model.md
  research: F:\todoapp_withai\specs\feat\setup-project-structure\research.md
  ticket: null
  adr: null
  pr: null
files_yaml:
  - F:\todoapp_withai\specs\3-advanced-features\tasks.md
tests_yaml: []
---

# Advanced Features Tasks Generation

## Prompt Text

```
/sp.tasks
Generate an actionable, dependency-ordered tasks.md for the feature based on available design artifacts.

Context for task generation: Generate an atomic, testable task breakdown for Phase I Advanced Level Todo App implementation. Each task must be implementable by Qwen Code in a single generation pass without manual intervention. Task Breakdown Requirements Structure each task EXACTLY as follows: ### T-ADV-001: [Descriptive Task Title] **Preconditions** - [List required state before task execution: e.g., "Intermediate-level codebase passing all tests", "specifications finalized in /specs/features/advanced-features.md"] **Scope** - Files to modify/create (exact paths) - Functions/classes to implement - Explicit boundaries (what this task does NOT include) **Acceptance Criteria** - [ ] Concrete, verifiable condition 1 (e.g., "parse_iso8601('2026-02-15T09:00:00Z') returns timezone-aware UTC datetime") - [ ] Concrete, verifiable condition 2 - [ ] Backward compatibility check (e.g., "All Intermediate tests pass unchanged") **Validation Command** ```bash # Single command to verify task completion pytest tests/test_temporal.py::test_parse_iso8601_utc_only -xvs References Spec: @specs/features/advanced-features.md §2 (Due Dates) ADR: ADR-003 (UTC-Only Datetime Enforcement) Plan: Phase A (Temporal Foundation) ## Required Task Sequence ### Foundation Layer (Temporal Primitives) 1. **T-ADV-001**: Implement UTC-only ISO 8601 parser with strict validation (reject naive datetimes) 2. **T-ADV-002**: Implement relative time formatter ("due in 2 hours", "overdue 5 minutes ago") 3. **T-ADV-003**: Create temporal.py module with validation tests covering edge cases (leap years, UTC offsets) ### Due Date Integration Layer 4. **T-ADV-004**: Enhance Task model with `due_date: datetime | None` field (default=None) preserving all existing defaults 5. **T-ADV-005**: Extend CLI parser with `--due "<iso8601>"` flag (optional, positionally safe with quoted strings) 6. **T-ADV-006**: Implement reminder check trigger BEFORE command output in CLI interface layer 7. **T-ADV-007**: Add `--due-before`/`--due-after` filter flags to query.py with UTC comparison logic 8. **T-ADV-008**: Implement `--sort due_date` with tasks without due dates appearing last ### Recurrence Engine Layer 9. **T-ADV-009**: Implement recurrence pattern calculator (daily=+1d, weekly=+7d, monthly=+30d) in recurrence.py 10. **T-ADV-010**: Create next occurrence generator preserving all metadata (priority/tags/due_date offset) 11. **T-ADV-011**: Intercept `complete_task()` via Feature Router to trigger recurrence BEFORE marking complete 12. **T-ADV-012**: Add `(R:pattern)` display indicator after tags in task listings ### Cross-Feature Integration Layer 13. **T-ADV-013**: Ensure `update` command preserves recurrence/due_date when flags omitted (no reset to default) 14. **T-ADV-014**: Implement combined filter logic: `list --priority high --due-after today --tag work` 15. **T-ADV-015**: Verify search command includes due_date fields in keyword matching (e.g., "tomorrow" → due tomorrow) ### Demo & Validation Layer 16. **T-ADV-016**: Create DEMO_SCRIPT.txt with exact 90-second command sequence (Basic → Intermediate → Advanced) 17. **T-ADV-017**: Implement dev-only `--simulate-time` flag gated behind `if os.getenv("DEMO_MODE")` for time manipulation 18. **T-ADV-018**: Write integration test executing full demo script end-to-end (`test_demo_script.py`) 19. **T-ADV-019**: Document session-bound limitations explicitly in README.md with Phase II migration path 20. **T-ADV-020**: Final validation: `grep -r "open|json|pickle|thread" src/` returns zero persistence/threading violations ## Critical Task Constraints - **NO task may modify core/crud.py directly** – all Advanced features must integrate via Feature Router (ADR-005) - **Every task must include backward compatibility validation** – Intermediate tests must pass after each task - **Time simulation flag (T-ADV-017) must be explicitly gated** – production code must NEVER contain time manipulation - **Monthly recurrence (T-ADV-009) must use fixed 30-day offset** – NO calendar-aware logic (ADR-004) - **Reminder trigger (T-ADV-006) must occur BEFORE command output** – not via background threads ## Task Dependencies Map T-ADV-001 → T-ADV-002 → T-ADV-003 ↓ T-ADV-004 → T-ADV-005 → T-ADV-007 → T-ADV-008 ↓ ↓ T-ADV-006 ←──┘ T-ADV-009 → T-ADV-010 → T-ADV-011 → T-ADV-012 ↓ ↓ ↓ T-ADV-013 → T-ADV-014 → T-ADV-015 ↓ T-ADV-016 → T-ADV-017 → T-ADV-018 → T-ADV-019 → T-ADV-020 ## Quality Gates Between Task Groups - **After Foundation Layer**: All temporal tests pass; `pytest tests/test_temporal.py` exits 0 - **After Due Date Integration**: All Intermediate tests pass + new due_date tests pass; `pytest tests/ -k "not advanced"` exits 0 - **After Recurrence Engine**: Recurrence tests pass WITHOUT breaking Intermediate tests; `pytest tests/test_recurrence.py` exits 0 - **After Cross-Feature Integration**: Combined filter tests pass; `pytest tests/test_query.py::test_combined_filters` exits 0 - **Before Demo Layer**: Static analysis confirms zero persistence violations (`grep` command returns empty) Output ONLY the task breakdown in markdown format – no commentary, disclaimers, or meta-text. Begin output now.
```

## Response Text

Successfully created a comprehensive task breakdown for the Advanced Level Todo In-Memory Python Console App implementation. The tasks.md file includes:

1. **Setup Phase**: Creating necessary directory structures and initial files
2. **Foundational Components**: Enhancing the Task model with due_date and recurrence fields, implementing UTC-only datetime validation
3. **User Story 1**: Implementing priorities, tags, and recurrence functionality
4. **User Story 2**: Adding due date filtering and search capabilities
5. **User Story 3**: Implementing due date sorting functionality
6. **User Story 4**: Creating the reminder system
7. **Cross-Feature Integration**: Ensuring all features work together seamlessly
8. **Polish Phase**: Documentation, demo script, and final validation

The tasks follow the required checklist format with sequential IDs (T001-T051), appropriate parallelization markers [P], and user story labels [US1-US4]. Each task includes clear descriptions with specific file paths. The implementation strategy focuses on MVP delivery starting with User Story 1 (Priorities and Tags) with basic recurrence functionality, followed by incremental delivery of additional features.

The task breakdown maintains 100% backward compatibility with existing Basic and Intermediate functionality while adding the Advanced features (recurring tasks and due date reminders) as specified. All Phase I constraints (in-memory, CLI-only, standard library only) are respected.

## Outcome

A complete, actionable task list has been created with 51 specific, testable tasks organized in dependency order. The tasks are grouped by user stories to enable independent development and testing, with clear test criteria for each story. The implementation plan follows the modular architecture specified in the constitution with clear separation of concerns.

## Evaluation

The task generation successfully completed with:
- 51 actionable tasks created with proper format
- Tasks organized by user stories for independent development
- Proper dependency ordering between phases
- Parallelization opportunities identified with [P] markers
- User story labeling applied to relevant tasks
- Comprehensive coverage of all required functionality
- Clear file paths specified for each task
- Implementation strategy defined with MVP approach
- Backward compatibility maintained throughout