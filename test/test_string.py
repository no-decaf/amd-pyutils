"""Test functions for the str module."""

from amd.util.string import camel_to_snake, snake_to_camel


class TestCamelToSnake:
    """Test the camel_to_snake function."""

    @staticmethod
    def test_no_uppercase():
        """Test converting snake case to camel case with no uppercase."""
        assert camel_to_snake("testcamelstring") == "testcamelstring"

    @staticmethod
    def test_uppercase():
        """Test converting snake case to camel case with uppercase."""
        assert camel_to_snake("testCamelString") == "test_camel_string"


class TestSnakeToCamel:
    """Test the snake_to_camel function."""

    @staticmethod
    def test_no_underscore():
        """Test converting snake case to camel case with no underscore."""
        assert snake_to_camel("testsnakestring") == "testsnakestring"

    @staticmethod
    def test_underscore():
        """Test converting snake case to camel case with an underscore."""
        assert snake_to_camel("test_snake_string") == "testSnakeString"
