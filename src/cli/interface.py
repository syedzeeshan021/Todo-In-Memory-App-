from ..core.crud import TaskManager
from ..features.priorities_tags import format_priority_display, format_tags_display
from ..ui.table import display_task_table
from ..ui.formatter import format_error_message, format_success_message
from datetime import datetime


class TodoInterface:
    """
    Handles command dispatch and output formatting for the todo application.
    """
    
    def __init__(self):
        """Initialize the TodoInterface with a TaskManager."""
        self.task_manager = TaskManager()
    
    def run_command(self, args):
        """
        Execute the command based on parsed arguments.
        
        Args:
            args: Parsed arguments from the CLI parser
            
        Returns:
            Result of the command execution
        """
        command = args.command
        
        if command == 'add':
            return self.add_task(args)
        elif command == 'list':
            return self.list_tasks(args)
        elif command == 'search':
            return self.search_tasks(args)
        elif command == 'update':
            return self.update_task(args)
        elif command == 'complete':
            return self.complete_task(args)
        elif command == 'delete':
            return self.delete_task(args)
        elif command == 'view':
            return self.view_task(args)
        else:
            raise ValueError(f"Unknown command: {command}")
    
    def add_task(self, args):
        """
        Add a new task with the given parameters.

        Args:
            args: Parsed arguments containing title, description, priority, tags, due date, and recurrence
        """
        # Process tags: args.tag might be a list of comma-separated strings
        tags = []
        for tag_str in args.tag:
            # Split comma-separated tags and add to the list
            tags.extend([tag.strip() for tag in tag_str.split(',') if tag.strip()])

        # Parse due date if provided
        due_date = None
        if args.due:
            try:
                from datetime import datetime
                due_date = datetime.fromisoformat(args.due.replace('Z', '+00:00'))
            except ValueError:
                print(format_error_message(f"Invalid due date format: {args.due}. Use ISO 8601 format (e.g., '2026-02-15T09:00:00')"))
                return

        try:
            task = self.task_manager.create_task(
                title=args.title,
                description=args.description,
                priority=args.priority,
                tags=tags,
                due_date=due_date,
                recurrence=args.recur
            )
            # Format the output to include due date and recurrence info if present
            due_str = f" Due: {due_date.strftime('%Y-%m-%d %H:%M')}" if due_date else ""
            recur_str = f" (R:{args.recur})" if args.recur else ""
            print(format_success_message(f"Task {task.id} added: [{self._get_priority_indicator(task.priority)}] {task.title} {format_tags_display(task.tags)}{due_str}{recur_str}"))
        except ValueError as e:
            print(format_error_message(str(e)))
    
    def list_tasks(self, args):
        """
        List tasks with optional filtering and sorting.

        Args:
            args: Parsed arguments containing filter and sort options
        """
        # Process tags: args.tag might be a list of comma-separated strings
        tags = []
        for tag_str in args.tag:
            # Split comma-separated tags and add to the list
            tags.extend([tag.strip() for tag in tag_str.split(',') if tag.strip()])

        # Parse due date filters if provided
        due_before = None
        if args.due_before:
            try:
                from datetime import datetime
                due_before = datetime.fromisoformat(args.due_before.replace('Z', '+00:00'))
            except ValueError:
                print(format_error_message(f"Invalid due date format: {args.due_before}. Use ISO 8601 format (e.g., '2026-02-15T09:00:00')"))
                return

        due_after = None
        if args.due_after:
            try:
                from datetime import datetime
                due_after = datetime.fromisoformat(args.due_after.replace('Z', '+00:00'))
            except ValueError:
                print(format_error_message(f"Invalid due date format: {args.due_after}. Use ISO 8601 format (e.g., '2026-02-15T09:00:00')"))
                return

        tasks = self.task_manager.list_tasks(
            status=args.status,
            priority=args.priority,
            tags=tags,
            sort_by=args.sort,
            due_before=due_before,
            due_after=due_after
        )

        if not tasks:
            print("No tasks found matching your filters")
            return

        # Use the new professional table display
        print(display_task_table(tasks))
    
    def search_tasks(self, args):
        """
        Search tasks by keyword with optional filtering and sorting.

        Args:
            args: Parsed arguments containing keyword and filter/sort options
        """
        # Process tags: args.tag might be a list of comma-separated strings
        tags = []
        for tag_str in args.tag:
            # Split comma-separated tags and add to the list
            tags.extend([tag.strip() for tag in tag_str.split(',') if tag.strip()])

        # Parse due date filters if provided
        due_before = None
        if args.due_before:
            try:
                from datetime import datetime
                due_before = datetime.fromisoformat(args.due_before.replace('Z', '+00:00'))
            except ValueError:
                print(format_error_message(f"Invalid due date format: {args.due_before}. Use ISO 8601 format (e.g., '2026-02-15T09:00:00')"))
                return

        due_after = None
        if args.due_after:
            try:
                from datetime import datetime
                due_after = datetime.fromisoformat(args.due_after.replace('Z', '+00:00'))
            except ValueError:
                print(format_error_message(f"Invalid due date format: {args.due_after}. Use ISO 8601 format (e.g., '2026-02-15T09:00:00')"))
                return

        tasks = self.task_manager.search_tasks(
            keyword=args.keyword,
            status=args.status,
            priority=args.priority,
            tags=tags,
            sort_by=args.sort
        )

        # Apply due date filters to search results
        if due_before:
            tasks = [task for task in tasks if task.due_date and task.due_date <= due_before]
        if due_after:
            tasks = [task for task in tasks if task.due_date and task.due_date >= due_after]

        if not tasks:
            print("No tasks found matching your search and filters")
            return

        # Use the new professional table display
        print(display_task_table(tasks))
    
    def update_task(self, args):
        """
        Update an existing task.

        Args:
            args: Parsed arguments containing task ID and new values
        """
        # Process tags: args.tag might be a list of comma-separated strings
        tags = []
        for tag_str in args.tag:
            # Split comma-separated tags and add to the list
            tags.extend([tag.strip() for tag in tag_str.split(',') if tag.strip()])

        # If no tags were provided via command line, don't update tags (preserve existing)
        if not args.tag:
            tags = None

        # Parse due date if provided
        due_date = None
        if args.due:
            try:
                from datetime import datetime
                due_date = datetime.fromisoformat(args.due.replace('Z', '+00:00'))
            except ValueError:
                print(format_error_message(f"Invalid due date format: {args.due}. Use ISO 8601 format (e.g., '2026-02-15T09:00:00')"))
                return

        # If no due date was provided via command line, don't update due date (preserve existing)
        if not args.due:
            due_date = None

        try:
            task = self.task_manager.update_task(
                task_id=args.id,
                title=args.title,
                description=args.description,
                priority=args.priority,
                tags=tags,
                due_date=due_date,
                recurrence=args.recur
            )

            if task:
                # Format the output to include due date and recurrence info if present
                due_str = f" Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}" if task.due_date else ""
                recur_str = f" (R:{task.recurrence})" if task.recurrence else ""
                print(format_success_message(f"Task {task.id} updated: [{self._get_priority_indicator(task.priority)}] {task.title} {format_tags_display(task.tags)}{due_str}{recur_str}"))
            else:
                print(format_error_message(f"Task {args.id} not found"))
        except ValueError as e:
            print(format_error_message(str(e)))
    
    def complete_task(self, args):
        """
        Mark a task as complete.

        Args:
            args: Parsed arguments containing task ID
        """
        # First get the task to check if it's recurring
        task = self.task_manager.get_task(args.id)
        if not task:
            print(format_error_message(f"Task {args.id} not found"))
            return

        # Complete the task
        completed_task = self.task_manager.toggle_completion(args.id)

        if completed_task:
            # If the task has recurrence, generate the next occurrence
            if completed_task.recurrence:
                from ..features.recurrence import generate_next_occurrence
                next_task = generate_next_occurrence(completed_task, self.task_manager)
                
                # Add the next occurrence to the task manager
                self.task_manager.tasks[next_task.id] = next_task
                
                print(format_success_message(f"Task {completed_task.id} completed! Next occurrence scheduled for {next_task.due_date.strftime('%Y-%m-%d %H:%M:%S') if next_task.due_date else 'N/A'}"))
            else:
                status = "completed" if completed_task.completed else "marked as pending"
                print(format_success_message(f"Task {completed_task.id} {status}"))
        else:
            print(format_error_message(f"Task {args.id} not found"))
    
    def delete_task(self, args):
        """
        Delete a task.
        
        Args:
            args: Parsed arguments containing task ID
        """
        success = self.task_manager.delete_task(args.id)
        
        if success:
            print(format_success_message(f"Task {args.id} deleted"))
        else:
            print(format_error_message(f"Task {args.id} not found"))
    
    def view_task(self, args):
        """
        View details of a specific task.

        Args:
            args: Parsed arguments containing task ID
        """
        task = self.task_manager.get_task(args.id)

        if task:
            status = "Completed" if task.completed else "Pending"
            print(format_success_message("Task Details:"))
            print(f"ID: {task.id}")
            print(f"Title: {task.title}")
            print(f"Description: {task.description}")
            print(f"Status: {status}")
            print(f"Priority: {task.priority}")
            print(f"Tags: {format_tags_display(task.tags) or 'None'}")
            print(f"Due Date: {task.due_date.strftime('%Y-%m-%d %H:%M:%S') if task.due_date else 'Not set'}")
            print(f"Recurrence: {task.recurrence or 'Not set'}")
            print(f"Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(format_error_message(f"Task {args.id} not found"))
    
    def _get_priority_indicator(self, priority):
        """
        Get the display indicator for a priority level.
        
        Args:
            priority: Priority level ("high", "medium", "low")
            
        Returns:
            String indicator for the priority
        """
        return format_priority_display(priority)