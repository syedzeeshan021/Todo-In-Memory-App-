"""
Table display module for structured output in the UI.
Provides functions for displaying tabular data in a professional format.
"""

from .formatter import pad_text


def calculate_column_widths(rows, padding=2):
    """
    Calculate the appropriate width for each column based on content.
    
    Args:
        rows (list): List of rows, each row is a list of column values
        padding (int): Padding to add to each column
        
    Returns:
        list: List of column widths
    """
    if not rows:
        return []
    
    num_cols = len(rows[0])
    col_widths = [0] * num_cols
    
    for row in rows:
        for i, cell in enumerate(row):
            cell_len = len(str(cell))
            if cell_len > col_widths[i]:
                col_widths[i] = cell_len
    
    # Add padding to each column
    col_widths = [width + padding for width in col_widths]
    
    return col_widths


def format_separator_line(col_widths, border_char='-', junction_char='+'):
    """
    Format a separator line for the table.
    
    Args:
        col_widths (list): List of column widths
        border_char (str): Character to use for borders
        junction_char (str): Character to use for junctions
        
    Returns:
        str: Formatted separator line
    """
    segments = [junction_char]
    for width in col_widths:
        segments.append(border_char * width)
        segments.append(junction_char)
    
    return ''.join(segments)


def format_row(cells, col_widths, align='left'):
    """
    Format a row with proper alignment and borders.
    
    Args:
        cells (list): List of cell values
        col_widths (list): List of column widths
        align (str): Default alignment for cells
        
    Returns:
        str: Formatted row
    """
    segments = ['|']
    for i, (cell, width) in enumerate(zip(cells, col_widths)):
        padded_cell = pad_text(str(cell), width - 1, align)  # -1 for space before |
        segments.append(padded_cell)
        segments.append('|')
    
    return ''.join(segments)


def display_table(rows, headers=None, align='left'):
    """
    Display a table with the given rows and optional headers.
    
    Args:
        rows (list): List of rows to display
        headers (list): Optional list of headers
        align (str): Default alignment for cells
        
    Returns:
        str: Formatted table as a string
    """
    if not rows and not headers:
        return "No data to display"
    
    # Prepare data with headers if provided
    table_data = []
    if headers:
        table_data.append(headers)
    table_data.extend(rows)
    
    if not table_data:
        return "No data to display"
    
    # Calculate column widths
    col_widths = calculate_column_widths(table_data)
    
    # Build the table
    table_lines = []
    
    for i, row in enumerate(table_data):
        # Add separator before header and after header (if there are data rows)
        if i == 0:  # First row (header)
            table_lines.append(format_separator_line(col_widths))
        
        table_lines.append(format_row(row, col_widths, align))
        
        # Add separator after header if there are data rows
        if i == 0 and len(table_data) > 1:
            table_lines.append(format_separator_line(col_widths))
    
    # Add final separator
    table_lines.append(format_separator_line(col_widths))
    
    return '\n'.join(table_lines)


def display_task_table(tasks, include_headers=True):
    """
    Display a table of tasks in a professional format.
    
    Args:
        tasks (list): List of task objects to display
        include_headers (bool): Whether to include column headers
        
    Returns:
        str: Formatted task table as a string
    """
    from .formatter import format_task_row
    
    if not tasks:
        return "No tasks found"
    
    # Prepare the table data
    table_rows = []
    
    # Add header row if requested
    if include_headers:
        header_row = format_task_row(None, include_header=True)
        table_rows.append(header_row)
    
    # Add data rows
    for task in tasks:
        row = format_task_row(task)
        table_rows.append(row)
    
    return display_table(table_rows[1:], headers=table_rows[0] if include_headers else None)