#!/usr/bin/env python3
"""
Main entry point for the Todo In-Memory Python Console App.
"""

from src.cli.parser import create_parser
from src.cli.interface import TodoInterface


def main():
    """Main function to run the todo application."""
    parser = create_parser()
    args = parser.parse_args()

    # If no command was provided, show help
    if not hasattr(args, 'command') or args.command is None:
        parser.print_help()
        return

    interface = TodoInterface()

    # If simulate-time is provided, set the system time accordingly
    if hasattr(args, 'simulate_time') and args.simulate_time:
        # For Phase I, we'll just print that simulation mode is active
        # In a real implementation, we would set a mock time for the application
        print(f"[INFO] Simulation mode active - time set to: {args.simulate_time}")

    # Check for reminders before executing any command
    from src.features.reminders import check_for_reminders
    reminders = check_for_reminders(list(interface.task_manager.tasks.values()))
    for reminder in reminders:
        print(reminder)

    # Execute the requested command
    interface.run_command(args)


if __name__ == "__main__":
    main()