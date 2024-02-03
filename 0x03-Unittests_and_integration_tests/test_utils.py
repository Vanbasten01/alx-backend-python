#!/usr/bin/env python3
"""Module for testing the access_nested_map function."""
import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    """Test case for the access_nested_map function."""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(
            self, nested_map: Mapping,
            path: Sequence,
            expected_result: Any):
        """Test the access_nested_map function."""
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
        ])
    def test_access_nested_map_exception(self, nested_map: Mapping,
                                         path: Sequence):
        """Test access_nested_map_exception function """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Unit tests for the get_json function."""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test whether get_json retrieves and returns
        JSON payload correctly."""
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response
        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Test case for the memoize decorator functionality."""
    def test_memoize(self):
        """Test the memoize decorator with a class method."""
        class TestClass:
            """A test class to demonstrate memoization."""
            def a_method(self):
                """Returns a constant value."""
                return 42

            @memoize
            def a_property(self):
                """Returns the result of the a_method method."""
                return self.a_method()

        test_instance = TestClass()
        with patch.object(test_instance, 'a_method') as mock_a_method:
            mock_a_method.return_value = 42
            result1 = test_instance.a_property
            result2 = test_instance.a_property

            mock_a_method.assert_called_once()
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)


if __name__ == "__main__":
    unittest.main()
