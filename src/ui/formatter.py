"""
Formatting utility module for professional display in the UI.
Provides functions for consistent formatting of UI elements.
"""

from .colors import colorize, get_priority_color, get_status_color, get_tag_color


def format_priority_indicator(priority):
    """
    Format the priority indicator with appropriate symbol and color.
    
    Args:
        priority (str): Priority level ("high", "medium", "low")
        
    Returns:
        str: Formatted priority indicator
    """
    if priority == "high":
        indicator = "🔴"  # Red circle for high priority
    elif priority == "medium":
        indicator = "🟡"  # Yellow circle for medium priority
    elif priority == "low":
        indicator = "🟢"  # Green circle for low priority
    else:
        indicator = "⚪"  # White circle for unknown priority
        
    color_code = get_priority_color(priority)
    return colorize(indicator, color_code)


def format_status_indicator(completed):
    """
    Format the status indicator with appropriate symbol and color.
    
    Args:
        completed (bool): Whether the task is completed
        
    Returns:
        str: Formatted status indicator
    """
    if completed:
        indicator = "X"  # X for completed
        color_code = get_status_color(True)
    else:
        indicator = "O"  # O for pending
        color_code = get_status_color(False)
        
    return colorize(indicator, color_code)


def format_tags_display(tags):
    """
    Format tags for display with appropriate color.
    
    Args:
        tags (list): List of tags
        
    Returns:
        str: Formatted tags string
    """
    if not tags:
        return ""
    
    # Colorize each tag
    colored_tags = [colorize(tag, get_tag_color()) for tag in tags]
    return f" [{', '.join(colored_tags)}]"


def format_task_row(task, include_header=False):
    """
    Format a task as a row for display in a table.

    Args:
        task: Task object with id, title, description, completed, priority, tags, due_date, recurrence
        include_header (bool): Whether to include column headers

    Returns:
        list: List of formatted columns for the task
    """
    if include_header:
        return ["ID", "Status", "Priority", "Title", "Tags", "Due Date", "Recurrence"]

    status = format_status_indicator(task.completed)
    priority = format_priority_indicator(task.priority)
    tags = format_tags_display(task.tags)
    due_date = task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else ""
    recurrence = f"(R:{task.recurrence})" if task.recurrence else ""

    return [str(task.id), status, priority, task.title, tags, due_date, recurrence]


def center_text(text, width):
    """
    Center text within a given width.
    
    Args:
        text (str): Text to center
        width (int): Width to center within
        
    Returns:
        str: Centered text
    """
    return text.center(width)


def pad_text(text, width, align='left'):
    """
    Pad text to a given width with specified alignment.
    
    Args:
        text (str): Text to pad
        width (int): Width to pad to
        align (str): Alignment ('left', 'right', 'center')
        
    Returns:
        str: Padded text
    """
    if align == 'right':
        return text.rjust(width)
    elif align == 'center':
        return text.center(width)
    else:  # left
        return text.ljust(width)


def format_error_message(message):
    """
    Format an error message with appropriate color and prefix.
    
    Args:
        message (str): Error message
        
    Returns:
        str: Formatted error message
    """
    from .colors import Colors
    return f"{colorize('[ERROR]', Colors.RED)} {colorize(message, Colors.BRIGHT_RED)}"


def format_success_message(message):
    """
    Format a success message with appropriate color and prefix.
    
    Args:
        message (str): Success message
        
    Returns:
        str: Formatted success message
    """
    from .colors import Colors
    return f"{colorize('[SUCCESS]', Colors.GREEN)} {colorize(message, Colors.BRIGHT_GREEN)}"


# Text-only mode for screen readers
TEXT_ONLY_MODE = False


def set_text_only_mode(enabled):
    """
    Enable or disable text-only mode for screen readers.
    
    Args:
        enabled (bool): Whether to enable text-only mode
    """
    global TEXT_ONLY_MODE
    TEXT_ONLY_MODE = enabled


def format_priority_indicator_text_only(priority):
    """
    Format the priority indicator for text-only mode.
    
    Args:
        priority (str): Priority level ("high", "medium", "low")
        
    Returns:
        str: Formatted priority indicator for text-only mode
    """
    if priority == "high":
        return "[HIGH PRIORITY]"
    elif priority == "medium":
        return "[MEDIUM PRIORITY]"
    elif priority == "low":
        return "[LOW PRIORITY]"
    else:
        return "[UNKNOWN PRIORITY]"


def format_status_indicator_text_only(completed):
    """
    Format the status indicator for text-only mode.
    
    Args:
        completed (bool): Whether the task is completed
        
    Returns:
        str: Formatted status indicator for text-only mode
    """
    if completed:
        return "[COMPLETED]"
    else:
        return "[PENDING]"


def format_priority_indicator(priority):
    """
    Format the priority indicator with appropriate symbol and color.
    
    Args:
        priority (str): Priority level ("high", "medium", "low")
        
    Returns:
        str: Formatted priority indicator
    """
    if TEXT_ONLY_MODE:
        return format_priority_indicator_text_only(priority)
    
    if priority == "high":
        indicator = "!!!"  # Exclamation marks for high priority
    elif priority == "medium":
        indicator = "!! "  # Two exclamation marks for medium priority
    elif priority == "low":
        indicator = "!  "  # One exclamation mark for low priority
    else:
        indicator = "   "  # Spaces for unknown priority
        
    color_code = get_priority_color(priority)
    return colorize(indicator, color_code)


def format_status_indicator(completed):
    """
    Format the status indicator with appropriate symbol and color.
    
    Args:
        completed (bool): Whether the task is completed
        
    Returns:
        str: Formatted status indicator
    """
    if TEXT_ONLY_MODE:
        return format_status_indicator_text_only(completed)
    
    if completed:
        indicator = "X"  # X for completed
        color_code = get_status_color(True)
    else:
        indicator = "O"  # O for pending
        color_code = get_status_color(False)
        
    return colorize(indicator, color_code)