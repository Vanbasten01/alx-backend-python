#!/usr/bin/env python3
"""This script tests the org method of the GithubOrgClient class."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, MagicMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for the org method of the GithubOrgClient class."""
    @parameterized.expand([
        ("google"),
        ("abc")
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test the org method of GithubOrgClient class."""
        test_inst = GithubOrgClient(org_name)
        test_inst.org()
        # Assert that the get_json method was called with the expected URL
        mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}")


if __name__ == "__main__":
    unittest.main()
