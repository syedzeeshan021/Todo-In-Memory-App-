"""
Unit tests for priority and tag functionality.
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.features.priorities_tags import normalize_priority, parse_tags_from_string, format_priority_display, format_tags_display


def test_priority_normalization():
    """Test priority normalization functionality."""
    assert normalize_priority("HIGH") == "high"
    assert normalize_priority("high") == "high"
    assert normalize_priority("High") == "high"
    assert normalize_priority("LOW") == "low"
    assert normalize_priority("medium") == "medium"
    
    try:
        normalize_priority("invalid")
        assert False, "Should raise ValueError for invalid priority"
    except ValueError:
        pass  # Expected
    
    print("✓ Priority normalization tests passed")


def test_tag_parsing():
    """Test tag parsing functionality."""
    assert parse_tags_from_string("") == []
    assert parse_tags_from_string("work") == ["work"]
    assert parse_tags_from_string("work, personal") == ["work", "personal"]
    assert parse_tags_from_string("work, personal, urgent") == ["work", "personal", "urgent"]
    assert parse_tags_from_string("  work  ,  personal  ") == ["work", "personal"]  # Test whitespace stripping
    assert parse_tags_from_string("work,,personal") == ["work", "personal"]  # Test empty tag handling
    
    print("✓ Tag parsing tests passed")


def test_formatting():
    """Test display formatting functionality."""
    assert format_priority_display("high") == "!"
    assert format_priority_display("medium") == "~"
    assert format_priority_display("low") == " "
    assert format_priority_display("invalid") == " "  # Default case
    
    assert format_tags_display([]) == ""
    assert format_tags_display(["work"]) == "(work)"
    assert format_tags_display(["work", "personal"]) == "(work, personal)"
    
    print("✓ Formatting tests passed")


if __name__ == "__main__":
    test_priority_normalization()
    test_tag_parsing()
    test_formatting()
    print("\nAll priority and tag functionality tests passed!")