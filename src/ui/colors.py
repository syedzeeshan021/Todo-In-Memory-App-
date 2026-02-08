"""
Color utility module for consistent color scheme in the UI.
Provides color codes for different elements of the UI.
"""

import sys


def supports_color():
    """
    Check if the terminal supports color output.

    Returns:
        bool: True if color is supported, False otherwise
    """
    # Check if running on Windows and if terminal supports ANSI codes
    if sys.platform.startswith('win'):
        import os
        # Check if we're in a terminal that supports colors
        return os.isatty(sys.stdout.fileno()) if hasattr(sys.stdout, 'fileno') else True
    return sys.stdout.isatty()


class Colors:
    """Class containing color codes for consistent UI coloring."""
    
    # Check if colors are supported
    COLOR_SUPPORTED = supports_color()
    
    # Color codes (only applied if terminal supports color)
    if COLOR_SUPPORTED:
        # Reset
        RESET = '\033[0m'
        
        # Text colors
        BLACK = '\033[30m'
        RED = '\033[31m'
        GREEN = '\033[32m'
        YELLOW = '\033[33m'
        BLUE = '\033[34m'
        MAGENTA = '\033[35m'
        CYAN = '\033[36m'
        WHITE = '\033[37m'
        
        # Bright text colors
        BRIGHT_BLACK = '\033[90m'
        BRIGHT_RED = '\033[91m'
        BRIGHT_GREEN = '\033[92m'
        BRIGHT_YELLOW = '\033[93m'
        BRIGHT_BLUE = '\033[94m'
        BRIGHT_MAGENTA = '\033[95m'
        BRIGHT_CYAN = '\033[96m'
        BRIGHT_WHITE = '\033[97m'
        
        # Background colors
        BG_BLACK = '\033[40m'
        BG_RED = '\033[41m'
        BG_GREEN = '\033[42m'
        BG_YELLOW = '\033[43m'
        BG_BLUE = '\033[44m'
        BG_MAGENTA = '\033[45m'
        BG_CYAN = '\033[46m'
        BG_WHITE = '\033[47m'
        
        # Bright background colors
        BG_BRIGHT_BLACK = '\033[100m'
        BG_BRIGHT_RED = '\033[101m'
        BG_BRIGHT_GREEN = '\033[102m'
        BG_BRIGHT_YELLOW = '\033[103m'
        BG_BRIGHT_BLUE = '\033[104m'
        BG_BRIGHT_MAGENTA = '\033[105m'
        BG_BRIGHT_CYAN = '\033[106m'
        BG_BRIGHT_WHITE = '\033[107m'
        
        # Styles
        BOLD = '\033[1m'
        DIM = '\033[2m'
        ITALIC = '\033[3m'
        UNDERLINE = '\033[4m'
        BLINK = '\033[5m'
        REVERSE = '\033[7m'
        STRIKETHROUGH = '\033[9m'
    else:
        # If colors are not supported, use empty strings
        RESET = ''
        BLACK = ''
        RED = ''
        GREEN = ''
        YELLOW = ''
        BLUE = ''
        MAGENTA = ''
        CYAN = ''
        WHITE = ''
        BRIGHT_BLACK = ''
        BRIGHT_RED = ''
        BRIGHT_GREEN = ''
        BRIGHT_YELLOW = ''
        BRIGHT_BLUE = ''
        BRIGHT_MAGENTA = ''
        BRIGHT_CYAN = ''
        BRIGHT_WHITE = ''
        BG_BLACK = ''
        BG_RED = ''
        BG_GREEN = ''
        BG_YELLOW = ''
        BG_BLUE = ''
        BG_MAGENTA = ''
        BG_CYAN = ''
        BG_WHITE = ''
        BG_BRIGHT_BLACK = ''
        BG_BRIGHT_RED = ''
        BG_BRIGHT_GREEN = ''
        BG_BRIGHT_YELLOW = ''
        BG_BRIGHT_BLUE = ''
        BG_BRIGHT_MAGENTA = ''
        BG_BRIGHT_CYAN = ''
        BG_BRIGHT_WHITE = ''
        BOLD = ''
        DIM = ''
        ITALIC = ''
        UNDERLINE = ''
        BLINK = ''
        REVERSE = ''
        STRIKETHROUGH = ''


def colorize(text, color_code):
    """
    Apply color to text if color is supported.
    
    Args:
        text (str): Text to colorize
        color_code (str): Color code to apply
        
    Returns:
        str: Colorized text (or original text if colors not supported)
    """
    if Colors.COLOR_SUPPORTED:
        return f"{color_code}{text}{Colors.RESET}"
    return text


def get_priority_color(priority):
    """
    Get the appropriate color for a priority level.
    
    Args:
        priority (str): Priority level ("high", "medium", "low")
        
    Returns:
        str: Color code for the priority
    """
    if priority == "high":
        return Colors.RED
    elif priority == "medium":
        return Colors.YELLOW
    elif priority == "low":
        return Colors.GREEN
    else:
        return Colors.WHITE


def get_status_color(completed):
    """
    Get the appropriate color for a task status.
    
    Args:
        completed (bool): Whether the task is completed
        
    Returns:
        str: Color code for the status
    """
    if completed:
        return Colors.GREEN
    else:
        return Colors.WHITE


def get_tag_color():
    """
    Get the appropriate color for tags.
    
    Returns:
        str: Color code for tags
    """
    return Colors.CYAN


def get_high_contrast_priority_color(priority):
    """
    Get the appropriate high contrast color for a priority level.
    
    Args:
        priority (str): Priority level ("high", "medium", "low")
        
    Returns:
        str: High contrast color code for the priority
    """
    if priority == "high":
        return Colors.BG_RED + Colors.WHITE  # White text on red background
    elif priority == "medium":
        return Colors.BG_YELLOW + Colors.BLACK  # Black text on yellow background
    elif priority == "low":
        return Colors.BG_GREEN + Colors.WHITE  # White text on green background
    else:
        return Colors.BG_WHITE + Colors.BLACK  # Black text on white background


def get_high_contrast_status_color(completed):
    """
    Get the appropriate high contrast color for a task status.
    
    Args:
        completed (bool): Whether the task is completed
        
    Returns:
        str: High contrast color code for the status
    """
    if completed:
        return Colors.BG_GREEN + Colors.WHITE  # White text on green background
    else:
        return Colors.BG_WHITE + Colors.BLACK  # Black text on white background