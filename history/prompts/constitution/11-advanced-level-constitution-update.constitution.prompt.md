---
id: 11
title: Advanced Level Constitution Update
stage: constitution
date_iso: 2026-02-08
surface: agent
model: Qwen Code
feature: todo-advanced-features
branch: feat/setup-project-structure
user: user
command: /sp.constitution
labels: ["constitution", "specification", "todo-app", "advanced"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - F:\todoapp_withai\.specify\memory\constitution.md
tests_yaml: []
---

# Advanced Level Constitution Update

## Prompt Text

```
/sp.constitution
You are an expert spec-driven development architect. Generate a constitution document for Phase I: Todo In-Memory Python Console App — Advanced Level that extends the existing intermediate-level constitution while maintaining strict backward compatibility with Basic + Intermediate functionality.
Context
Basic level implemented: add/delete/update/view tasks + mark complete/incomplete
Intermediate level added: priorities/tags, search/filter/sort (all in-memory, CLI-only)
Advanced level must ADD (not replace) these capabilities within Phase I constraints:
Recurring Tasks: Session-bound recurrence patterns (daily/weekly/monthly) that auto-generate next occurrence upon completion within the same running session only
Due Dates & Reminders: ISO 8601 datetime support with console-based reminder alerts (NO browser notifications – Phase I is CLI-only)
Critical Phase I constraints preserved:
Strictly in-memory storage (NO file/database persistence)
CLI/console interface only (NO browser/frontend dependencies)
Python 3.13+ standard library only (NO external libraries)
UV environment management + Qwen Code for 100% implementation
Constitution Requirements
Structure the output EXACTLY as follows:                                                                 # Todo In-Memory Python Console App Constitution (Advanced Level)

## Core Principles
[Six principles total. First three MUST mirror prior levels: Spec-Driven Development, Agentic Workflow, No Manual Coding. Add three NEW principles specific to Advanced level: Session-Bound Recurrence Integrity, Console-First Reminder Design, Temporal Data Safety]

## Rules and Regulations
[Four subsections:]
### Required Advanced Features (In-Memory Implementation)
- Detail recurrence patterns with explicit session-bound constraints (e.g., "daily recurrence only generates next occurrence while app remains running")
- Specify due date format (ISO 8601) and console reminder mechanics (e.g., "reminder printed on next user interaction after due time passes")
- Define recurrence + due date interactions (e.g., "next occurrence inherits due date offset from original")

### Technical Constraints
- Reaffirm in-memory storage with explicit prohibition against background threads/services that imply persistence
- CLI interface rules: preserve all prior command syntax while adding optional `--due` and `--recur` flags
- Technology stack: UV, Python 3.13+, Qwen Code, Spec-Kit Plus — NO external libraries (including dateutil, croniter)
- Explicit prohibition: NO browser APIs, NO system notifications, NO background daemons

### Testing Requirements
- Mandate tests for session-bound recurrence edge cases (app exit before recurrence triggers)
- Require temporal boundary tests (due dates in past/future, timezone handling via UTC only)
- Test recurrence + priority/tag/filter interactions

### Repository Structure
- Show updated directory tree with /src/features/recurrence.py and /src/features/due_dates.py
- Require /specs/features/advanced-features.md specification file

## Governance
- State backward compatibility as non-negotiable (all Basic + Intermediate commands must work unchanged)
- Declare session-bound nature of Advanced features as intentional design constraint (not a bug)
- Require explicit documentation of temporal limitations in README.md
- Declare violations invalidate Advanced implementation phase                                             Critical Constraints
DO NOT remove or weaken any Basic/Intermediate requirements
DO NOT permit file/database persistence or background services (strictly in-memory, single-process)
DO NOT allow browser/frontend dependencies (Phase I is CLI-only – reinterpret "notifications" as console alerts)
DO NOT permit external libraries for date parsing (use datetime.fromisoformat only)
Constitution must be self-contained and executable by development teams without external clarification
Output ONLY the constitution document — no commentary, disclaimers, or meta-text
Begin output now.
```

## Response Text

Successfully updated the project constitution to include advanced level features while maintaining backward compatibility with basic and intermediate functionality. The updated constitution includes:

1. Three new core principles specific to the advanced level:
   - Session-Bound Recurrence Integrity
   - Console-First Reminder Design
   - Temporal Data Safety

2. Detailed requirements for advanced features:
   - Recurring tasks with session-bound constraints
   - Due dates and reminders using ISO 8601 format
   - Interactions between recurrence and due dates

3. Technical constraints reaffirming in-memory storage and CLI-only interface
4. Testing requirements for temporal boundaries and session-bound behavior
5. Updated repository structure with new files for recurrence and due dates
6. Governance rules maintaining backward compatibility and session-bound design

The constitution version was incremented from 1.1.0 to 1.2.0 to reflect the addition of new principles and advanced features while maintaining all existing functionality.

## Outcome

The constitution document has been successfully updated to version 1.2.0 with advanced level features while preserving all basic and intermediate functionality requirements. The document is ready for use in implementing the advanced features of the Todo In-Memory Python Console App.

## Evaluation

The constitution update successfully completed with:
- Version incremented from 1.1.0 to 1.2.0 (minor version bump for new features)
- Three new core principles added for advanced level
- All required advanced features specified with session-bound constraints
- Backward compatibility maintained with basic and intermediate functionality
- Technical constraints properly specified for advanced features
- Testing requirements updated for temporal features
- Repository structure updated with new files
- Governance rules updated to reflect advanced level requirements
- All critical constraints preserved