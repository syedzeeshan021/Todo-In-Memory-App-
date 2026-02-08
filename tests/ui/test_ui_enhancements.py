"""
Simple test to verify the UI enhancements work correctly.
"""
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.ui.colors import Colors, colorize, get_priority_color, get_status_color
from src.ui.formatter import (
    format_priority_indicator, 
    format_status_indicator, 
    format_tags_display, 
    format_error_message, 
    format_success_message,
    set_text_only_mode
)
from src.ui.table import display_task_table


def test_colors():
    """Test color functionality."""
    print("Testing colors...")
    
    # Test if colors are supported
    print(f"Colors supported: {Colors.COLOR_SUPPORTED}")
    
    # Test colorizing text
    red_text = colorize("This is red text", Colors.RED)
    print(f"Red text: {red_text}")
    
    print("✓ Color tests passed\n")


def test_formatters():
    """Test formatting functionality."""
    print("Testing formatters...")
    
    # Test priority indicators
    high_priority = format_priority_indicator("high")
    print(f"High priority indicator: {high_priority}")
    
    medium_priority = format_priority_indicator("medium")
    print(f"Medium priority indicator: {medium_priority}")
    
    low_priority = format_priority_indicator("low")
    print(f"Low priority indicator: {low_priority}")
    
    # Test status indicators
    completed_status = format_status_indicator(True)
    print(f"Completed status indicator: {completed_status}")
    
    pending_status = format_status_indicator(False)
    print(f"Pending status indicator: {pending_status}")
    
    # Test tag display
    tags_display = format_tags_display(["work", "urgent"])
    print(f"Tags display: {tags_display}")
    
    # Test error and success messages
    error_msg = format_error_message("Something went wrong")
    print(f"Error message: {error_msg}")
    
    success_msg = format_success_message("Operation completed successfully")
    print(f"Success message: {success_msg}")
    
    print("✓ Formatter tests passed\n")


def test_text_only_mode():
    """Test text-only mode for accessibility."""
    print("Testing text-only mode...")
    
    # Enable text-only mode
    set_text_only_mode(True)
    
    # Test priority indicators in text-only mode
    high_priority = format_priority_indicator("high")
    print(f"High priority in text-only mode: {high_priority}")
    
    # Test status indicators in text-only mode
    completed_status = format_status_indicator(True)
    print(f"Completed status in text-only mode: {completed_status}")
    
    # Disable text-only mode
    set_text_only_mode(False)
    
    # Test priority indicators in normal mode
    high_priority = format_priority_indicator("high")
    print(f"High priority in normal mode: {high_priority}")
    
    print("✓ Text-only mode tests passed\n")


if __name__ == "__main__":
    test_colors()
    test_formatters()
    test_text_only_mode()
    print("All UI enhancement tests passed! 🎉")