<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles: None (new constitution)
Added sections: Core Principles I-VI, Rules and Regulations, Technical Constraints, Repository Structure, Governance
Removed sections: None
Templates requiring updates: ⚠ pending (.specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md)
Follow-up TODOs: None
-->

# Todo In-Memory Python Console App Constitution

## Core Principles

### I. Spec-Driven Development
All features must originate from a written specification. No implementation without a spec, plan, and tasks. This ensures clear requirements, testable outcomes, and prevents scope creep during development. Intermediate features must be specified before any modification to existing code.

### II. Agentic Workflow
Follow the sequence strictly: Write spec → Clarify ambiguities → Generate plan → Break into tasks → Implement via AI tools (Qwen Code). Iterations must be documented in /specs/history/. This maintains discipline when extending the existing codebase with intermediate functionality.

### III. No Manual Coding
Developers (human or AI) must not write code directly. All code generation and modifications happen exclusively through Qwen Code. Refine specifications until Qwen Code produces correct output—never bypass the spec-driven loop or manually edit generated code.

### IV. Backward Compatibility
All intermediate features must preserve 100% compatibility with existing basic functionality. Users must be able to:
- Execute all basic commands (add, list, update, delete, complete) without encountering new required fields
- Use the application without engaging intermediate features
- Experience zero breaking changes to existing command syntax or behavior

### V. Enhanced Modularity
Intermediate features must be implemented with strict separation of concerns:
- Core CRUD operations remain in /src/core/
- Priority/tag logic resides in /src/features/priorities_tags.py
- Search/filter/sort logic resides in /src/features/query.py
- CLI parser must route commands to appropriate modules without tight coupling

### VI. Feature Interaction Safety
All combinations of intermediate features must be explicitly tested and specified:
- Filtering completed high-priority tasks with specific tags
- Sorting filtered results by multiple criteria
- Searching within filtered subsets
- Edge cases involving empty tags, mixed-case inputs, and special characters

## Rules and Regulations

### Required Intermediate Features (In-Memory Implementation)

#### Priorities & Tags/Categories
- Three priority levels: high, medium, low (default: medium when not specified)
- Custom tags/categories as comma-separated strings (e.g., work,urgent)
- Display indicators in task listings:
  - [!] prefix for high priority
  - [~] prefix for medium priority (optional display)
  - [ ] prefix for low priority
- Tags displayed in parentheses after description: (work, personal)
- Priority/tag assignment optional during add and update operations

#### Search & Filter
- Keyword search across title and description fields (case-insensitive partial match)
- Filter combinations with optional CLI flags:
  - --status [all|pending|completed] (default: all)
  - --priority [high|medium|low|all] (default: all)
  - --tag <tag> (exact or partial tag match)
- Support chained filters in single command:
  - Example: list --status pending --priority high --tag work
  - Example: search "meeting" --status pending
- Default list command shows all tasks without filters applied

#### Sort Tasks
- Sort options via --sort flag:
  - created (chronological by creation time, default)
  - priority (high → medium → low)
  - title (A→Z alphabetical)
- Tie-breaking rules:
  - Priority sort: tasks with same priority sorted by creation time (newest first)
  - Title sort: case-insensitive alphabetical order
- Sort preference applies only within current command execution (session-persistent but not persisted between runs—strictly in-memory)

## Technical Constraints

### Storage
- Strictly in-memory storage using Python data structures (lists/dicts)
- Explicit prohibition: No file I/O, no database connections, no environment variables for persistence
- Task IDs must remain stable within session but reset on application restart
- All state must reside in Python objects within the running process

### CLI Interface
- Preserve all basic command syntax unchanged:
  - add "Title" "Description"
  - list
  - complete 3
  - delete 2
  - update 1 "New Title" "New Desc"
- Add optional flags to list and search commands only:
  - Flags must be optional; commands work without flags
  - Flag syntax: --flag value or --flag=value
  - Implement search <keyword> command with same filter/sort flags as list
- User experience must remain intuitive; help text (--help) required for all commands

### Technology Stack
- UV for environment management and dependency isolation
- Python 3.13+ exclusively
- Qwen Code for 100% of implementation and modifications
- Spec-Kit Plus for specification management
- Standard library only—no external dependencies permitted

## Testing Requirements

### Unit Tests
- Test all intermediate features in isolation:
  - Priority assignment and display logic
  - Tag parsing, storage, and matching
  - Search keyword matching across fields
  - Filter combinations (status + priority + tag)
  - Sort stability and tie-breaking behavior
- Test feature interactions:
  - Filtered results correctly sorted
  - Search within filtered subsets
  - Priority display with tags present
- Edge case coverage:
  - Empty tag strings and whitespace handling
  - Mixed-case priority values (HIGH vs high)
  - Special characters in search terms (@#$%)
  - Tasks with identical titles/priorities

### Integration Tests
- Demonstrate complete user workflows:
  - Add task with priority/tag → List filtered view → Search within results → Sort output
  - Update task to change priority → Verify display updates correctly
  - Chain multiple filters with sort in single command
- Verify backward compatibility:
  - Basic commands function identically to pre-intermediate implementation
  - No regression in core CRUD operations

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
│   │   └── intermediate-features.md  # NEW: Detailed spec for priorities, tags, search, filter, sort
│   └── architecture/
│       └── in-memory-design.md  # Updated with intermediate feature integration
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py            # Enhanced Task model with priority/tags fields
│   │   └── crud.py              # Basic CRUD operations (unchanged interface)
│   ├── features/
│   │   ├── __init__.py
│   │   ├── priorities_tags.py   # Priority/tag assignment and validation
│   │   └── query.py             # Search, filter, and sort logic
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── parser.py            # Enhanced argument parser with flags
│   │   └── interface.py         # Command dispatch and output formatting
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── test_core.py             # Basic CRUD tests (unchanged)
│   ├── test_priorities_tags.py  # Priority/tag logic tests
│   ├── test_query.py            # Search/filter/sort tests
│   └── test_integration.py      # Feature interaction tests
├── QWEN.md                      # Qwen Code usage instructions and project context
├── README.md                    # Setup instructions (UV setup, running app)
└── pyproject.toml               # UV configuration with Python 3.13 constraint
```

## Governance
This constitution governs the extension of Phase I (In-Memory Console App) with intermediate features while maintaining strict adherence to spec-driven development principles. All implementations must:
- Preserve 100% backward compatibility—basic commands must function identically to the completed basic-level implementation
- Follow the agentic workflow without manual coding exceptions—Qwen Code must generate 100% of new and modified code
- Document all specification iterations in /specs/history/ with timestamps and change rationales
- Demonstrate all intermediate features and their interactions in the 90-second demo video

Critical Enforcement Rules:
- Any implementation that breaks basic functionality invalidates the entire intermediate phase
- Any manual code edits (outside Qwen Code generation) invalidate the submission
- Any persistence mechanism (file/database) violates the in-memory constraint and invalidates the phase
- All feature interactions must be explicitly specified before implementation—no emergent behavior allowed

Amendments to this constitution require explicit documentation in /specs/history/ with justification tied to user experience constraints or technical infeasibility.

**Version**: 1.1.0 | **Ratified**: TODO(RATIFICATION_DATE): Date of original adoption | **Last Amended**: 2026-02-08