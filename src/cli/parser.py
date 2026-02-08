import argparse


def create_parser():
    """
    Create and configure the argument parser for the todo application.
    
    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        prog='todo',
        description='Todo In-Memory Python Console App with intermediate features',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s add "Buy groceries" "Milk, bread, eggs"
  %(prog)s add "High priority task" "Description" --priority high --tag work,urgent
  %(prog)s list
  %(prog)s list --status pending --priority high
  %(prog)s search "meeting" --status pending --tag work
  %(prog)s update 1 "Updated title" "Updated description" --priority low
  %(prog)s complete 1
  %(prog)s delete 1
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands', required=False)
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new task')
    add_parser.add_argument('title', help='Task title')
    add_parser.add_argument('description', help='Task description')
    add_parser.add_argument('--priority', help='Task priority (high, medium, low)',
                           choices=['high', 'medium', 'low'], default='medium')
    add_parser.add_argument('--tag', help='Comma-separated tags for the task',
                           type=str, action='append', default=[])
    add_parser.add_argument('--due', help='Due date in ISO 8601 format (e.g., "2026-02-15T09:00:00")',
                           type=str, default=None)
    add_parser.add_argument('--recur', help='Recurrence pattern (daily, weekly, monthly)',
                           choices=['daily', 'weekly', 'monthly'], default=None)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all tasks')
    list_parser.add_argument('--status', help='Filter by status',
                            choices=['all', 'pending', 'completed'], default='all')
    list_parser.add_argument('--priority', help='Filter by priority',
                            choices=['all', 'high', 'medium', 'low'], default='all')
    list_parser.add_argument('--tag', help='Filter by tag (can specify multiple times for OR condition)',
                            type=str, action='append', default=[])
    list_parser.add_argument('--due-before', help='Show tasks due before this date (ISO 8601 format)',
                            type=str, default=None)
    list_parser.add_argument('--due-after', help='Show tasks due after this date (ISO 8601 format)',
                            type=str, default=None)
    list_parser.add_argument('--sort', help='Sort by option',
                            choices=['created', 'priority', 'title', 'due_date'], default='created')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search tasks by keyword')
    search_parser.add_argument('keyword', help='Keyword to search for')
    search_parser.add_argument('--status', help='Filter by status',
                              choices=['all', 'pending', 'completed'], default='all')
    search_parser.add_argument('--priority', help='Filter by priority',
                              choices=['all', 'high', 'medium', 'low'], default='all')
    search_parser.add_argument('--tag', help='Filter by tag (can specify multiple times for OR condition)',
                               type=str, action='append', default=[])
    search_parser.add_argument('--due-before', help='Show tasks due before this date (ISO 8601 format)',
                              type=str, default=None)
    search_parser.add_argument('--due-after', help='Show tasks due after this date (ISO 8601 format)',
                              type=str, default=None)
    search_parser.add_argument('--sort', help='Sort by option',
                              choices=['created', 'priority', 'title', 'due_date'], default='created')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update an existing task')
    update_parser.add_argument('id', type=int, help='Task ID')
    update_parser.add_argument('title', help='New task title')
    update_parser.add_argument('description', help='New task description')
    update_parser.add_argument('--priority', help='New task priority (high, medium, low)',
                              choices=['high', 'medium', 'low'])
    update_parser.add_argument('--tag', help='New comma-separated tags for the task',
                              type=str, action='append', default=[])
    update_parser.add_argument('--due', help='New due date in ISO 8601 format (e.g., "2026-02-15T09:00:00")',
                              type=str, default=None)
    update_parser.add_argument('--recur', help='New recurrence pattern (daily, weekly, monthly)',
                              choices=['daily', 'weekly', 'monthly'], default=None)
    
    # Complete command
    complete_parser = subparsers.add_parser('complete', help='Mark a task as complete')
    complete_parser.add_argument('id', type=int, help='Task ID')
    
    # Delete command
    delete_parser = subparsers.add_parser('delete', help='Delete a task')
    delete_parser.add_argument('id', type=int, help='Task ID')
    
    # View command
    view_parser = subparsers.add_parser('view', help='View a specific task')
    view_parser.add_argument('id', type=int, help='Task ID')
    
    # Add global --simulate-time flag for demo purposes
    parser.add_argument('--simulate-time', help='Simulate time for demo purposes (ISO 8601 format, e.g., "2026-02-15T10:05:00")',
                       type=str, default=None)
    
    return parser