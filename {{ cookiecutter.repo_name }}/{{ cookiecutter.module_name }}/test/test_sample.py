"""
Sample test module to demonstrate pytest testing framework.

This module contains basic example tests that verify the testing
infrastructure is properly configured.
"""

import pytest


def test_simple_assertion():
    """Test basic assertion."""
    assert 1 + 1 == 2


def test_string_operations():
    """Test string operations."""
    result = "hello world"
    assert result.startswith("hello")
    assert result.endswith("world")
    assert len(result) == 11


def test_list_operations():
    """Test list operations."""
    data = [1, 2, 3, 4, 5]
    assert len(data) == 5
    assert sum(data) == 15
    assert max(data) == 5


def test_dictionary_operations():
    """Test dictionary operations."""
    config = {"name": "test", "version": "1.0", "enabled": True}
    assert "name" in config
    assert config["version"] == "1.0"
    assert config["enabled"] is True


@pytest.mark.parametrize("input_value,expected", [
    (0, 0),
    (1, 1),
    (2, 4),
    (3, 9),
    (4, 16),
])
def test_square_function(input_value, expected):
    """Test square function with parametrized inputs."""
    result = input_value ** 2
    assert result == expected


def test_exception_handling():
    """Test exception handling."""
    with pytest.raises(ZeroDivisionError):
        _ = 1 / 0

    with pytest.raises(KeyError):
        data = {}
        _ = data["missing_key"]
