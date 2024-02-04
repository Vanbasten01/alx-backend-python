#!/usr/bin/env python3
"""This script tests the org method of the GithubOrgClient class."""

import unittest
from parameterized import parameterized
from unittest.mock import patch, PropertyMock
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
        mock_get_json.assert_called_once_with(
                f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """Test the _public_repos_url property of GithubOrgClient."""
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock:
            payload = {"repos_url": "url"}
            mock.return_value = payload
            client = GithubOrgClient('test_org')
            result = client._public_repos_url
            self.assertEqual(result, payload["repos_url"])


if __name__ == "__main__":
    unittest.main()
