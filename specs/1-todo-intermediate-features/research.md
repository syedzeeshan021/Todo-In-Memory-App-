# Research for Todo In-Memory Python Console App - Intermediate Features

## Overview
This research document addresses the technical decisions and clarifications needed for implementing the intermediate features (priorities, tags, search, filter, sort) for the Todo In-Memory Python Console App while maintaining 100% backward compatibility.

## Decision: CLI Argument Parsing
**Rationale**: Need to select an appropriate method for parsing command-line arguments that supports optional flags while maintaining backward compatibility with existing commands.

**Decision**: Use Python's built-in `argparse` module which is part of the standard library and provides robust support for both positional and optional arguments.

**Alternatives considered**:
- Custom parsing with sys.argv: Would require more manual work and error handling
- Third-party libraries like click: Would violate the "standard library only" constraint

## Decision: In-Memory Data Storage Implementation
**Rationale**: Need to store tasks in memory with support for the new properties (priority, tags) while maintaining performance requirements.

**Decision**: Use Python lists and dictionaries for in-memory storage, with a central task manager class to handle all CRUD operations.

**Alternatives considered**:
- Using classes with static variables: Would be harder to manage
- Global variables: Would make testing difficult

## Decision: Task ID Management
**Rationale**: Need to ensure task IDs remain stable within a session and follow a predictable pattern.

**Decision**: Use auto-incrementing integer IDs starting from 1, managed by the task manager.

**Alternatives considered**:
- UUIDs: Would be unnecessarily complex for this use case
- Random integers: Would not be sequential and predictable

## Decision: String Matching Algorithm for Search
**Rationale**: Need to implement case-insensitive partial matching for search functionality.

**Decision**: Use Python's `in` operator with lowercased strings for simple substring matching.

**Alternatives considered**:
- Regular expressions: Would be overkill for simple partial matching
- Levenshtein distance: Would be too complex for this requirement

## Decision: Tag Parsing and Storage
**Rationale**: Need to parse comma-separated tags and store them appropriately.

**Decision**: Split tag strings on commas, strip whitespace, and store as a list of strings in the task object.

**Alternatives considered**:
- Using a single string with comma separators: Would make filtering more complex
- Using sets for tags: Would lose the order, though order isn't critical for tags

## Decision: Sorting Algorithm
**Rationale**: Need to implement sorting by different criteria with proper tie-breaking rules.

**Decision**: Use Python's built-in `sorted()` function with custom key functions for each sort type, implementing multi-level sorting where needed for tie-breaking.

**Alternatives considered**:
- Custom sorting algorithms: Would be unnecessarily complex
- Multiple separate lists: Would waste memory and complicate updates

## Decision: Filter Combination Logic
**Rationale**: Need to implement AND logic for combining multiple filters.

**Decision**: Apply filters sequentially, where each filter reduces the result set further.

**Alternatives considered**:
- Complex boolean expressions: Would be harder to implement and debug
- Separate filter functions: Would require more complex coordination