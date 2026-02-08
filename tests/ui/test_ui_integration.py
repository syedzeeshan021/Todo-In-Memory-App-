"""
Integration test to verify UI enhancements work with the full application.
"""
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.core.models import Task
from src.ui.table import display_task_table
from src.ui.formatter import format_success_message, format_error_message


def test_full_integration():
    """Test that UI enhancements work with the full application."""
    print("Testing full UI integration...")
    
    # Create some sample tasks
    task1 = Task(id=1, title="High Priority Task", description="This is a high priority task", priority="high", tags=["work", "urgent"])
    task2 = Task(id=2, title="Medium Priority Task", description="This is a medium priority task", priority="medium", tags=["personal"])
    task3 = Task(id=3, title="Low Priority Task", description="This is a low priority task", priority="low", tags=["later"])
    task4 = Task(id=4, title="Completed Task", description="This task is completed", priority="medium", tags=["done"], completed=True)
    
    tasks = [task1, task2, task3, task4]
    
    # Test table display
    print("Displaying tasks in professional table format:")
    print(display_task_table(tasks))
    
    # Test success and error messages
    print(format_success_message("Tasks displayed successfully"))
    print(format_error_message("No errors detected"))
    
    print("✓ Full integration test passed\n")


if __name__ == "__main__":
    test_full_integration()
    print("UI enhancement integration test passed! 🎉")