# Research for Todo In-Memory Python Console App (Advanced Level)

## Overview

This research document addresses the technical decisions and clarifications needed for implementing the advanced features (recurring tasks and due date reminders) for the Todo In-Memory Python Console App while maintaining 100% backward compatibility.

## Decision: Datetime Handling Strategy

**Rationale**: Need to handle ISO 8601 datetime strings for due dates while ensuring timezone consistency across the application.

**Decision**: Use Python's built-in `datetime.fromisoformat()` for parsing ISO 8601 strings with explicit UTC enforcement. All datetime operations will be performed in UTC to avoid timezone complications.

**Alternatives considered**:
- Using third-party libraries like `pytz` or `dateutil`: Would violate the "standard library only" constraint
- Manual parsing: Would be error-prone and reinvent existing functionality
- Naive datetime objects: Would lead to timezone-related bugs

## Decision: Recurrence Calculation Method

**Rationale**: Need to calculate next occurrence dates for recurring tasks while maintaining simplicity within standard library constraints.

**Decision**: Use fixed interval approach for recurrence calculation:
- Daily: current date + 1 day
- Weekly: current date + 7 days  
- Monthly: current date + 30 days (fixed interval, not calendar-aware)

**Alternatives considered**:
- Calendar-aware months: Would require complex date arithmetic beyond standard library
- Cron-like expressions: Would add unnecessary complexity for basic recurrence needs
- Fixed day-of-week/month: Would require more complex state tracking

## Decision: Reminder Trigger Mechanism

**Rationale**: Need to implement reminder functionality without background processes while maintaining the CLI-only constraint.

**Decision**: Reminders trigger on next user interaction after due time passes. The system will check for overdue tasks before displaying output for any command.

**Alternatives considered**:
- Background threads: Would violate the single-process constraint and imply persistence
- Scheduled tasks: Would require external scheduler and violate in-memory constraint
- Polling mechanism: Would consume resources unnecessarily

## Decision: CLI Argument Extension

**Rationale**: Need to extend existing CLI commands with new flags while preserving all existing functionality.

**Decision**: Use argparse with optional flags that don't interfere with existing command structure. New flags will be prefixed with `--` and will have sensible defaults that preserve existing behavior.

**Alternatives considered**:
- Subcommand approach: Would require changing existing command syntax
- Positional arguments: Would break existing command structure
- Configuration files: Would violate the in-memory constraint

## Decision: Recurrence Termination

**Rationale**: Need to handle how users can stop recurring tasks without complex state management.

**Decision**: No automatic mechanism to terminate recurrence after creation. Users must delete the recurring task and optionally create a new non-recurring task.

**Alternatives considered**:
- Adding a --no-recur flag: Would add complexity to the update command
- Occurrence limits: Would require additional fields and state tracking
- Manual disable mechanism: Would require additional command or flag

## Decision: Reminder Frequency

**Rationale**: Need to balance user awareness of overdue tasks with avoiding excessive notifications.

**Decision**: Reminders appear on every command execution for overdue tasks until they are completed or the due date is modified.

**Alternatives considered**:
- One-time reminders: Would require additional state tracking to mark tasks as "reminded"
- Periodic reminders (hourly/daily): Would require background processes
- Summary reminders: Would be more complex to implement and less immediate