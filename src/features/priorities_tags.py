"""
Module for handling priority and tag operations in the todo application.
This includes validation, normalization, and display formatting.
"""


def normalize_priority(priority_input):
    """
    Normalize priority input to lowercase and validate it.
    
    Args:
        priority_input: Raw priority input from user
        
    Returns:
        str: Normalized priority value ("high", "medium", or "low")
        
    Raises:
        ValueError: If the priority is not valid
    """
    if not isinstance(priority_input, str):
        raise ValueError(f"Priority must be a string, got {type(priority_input).__name__}")
    
    normalized = priority_input.lower().strip()
    
    if normalized not in ["high", "medium", "low"]:
        raise ValueError(f"Invalid priority: '{priority_input}'. Must be one of 'high', 'medium', 'low'")
    
    return normalized


def parse_tags_from_string(tag_string):
    """
    Parse a comma-separated string of tags into a list.
    
    Args:
        tag_string: Comma-separated string of tags
        
    Returns:
        list: List of individual tags with whitespace stripped
    """
    if not tag_string:
        return []
    
    if not isinstance(tag_string, str):
        raise ValueError(f"Tags must be provided as a string, got {type(tag_string).__name__}")
    
    # Split by comma and strip whitespace from each tag
    tags = [tag.strip() for tag in tag_string.split(',')]
    
    # Filter out empty tags
    tags = [tag for tag in tags if tag]
    
    return tags


def format_priority_display(priority):
    """
    Format priority for display purposes.
    
    Args:
        priority: Priority level ("high", "medium", "low")
        
    Returns:
        str: Display indicator for the priority
    """
    if priority == "high":
        return "!"
    elif priority == "medium":
        return "~"
    elif priority == "low":
        return " "
    else:
        # Default to low priority indicator for invalid values
        return " "


def format_tags_display(tags):
    """
    Format tags for display purposes.
    
    Args:
        tags: List of tags
        
    Returns:
        str: Formatted string of tags in parentheses
    """
    if not tags:
        return ""
    return "(" + ", ".join(tags) + ")"