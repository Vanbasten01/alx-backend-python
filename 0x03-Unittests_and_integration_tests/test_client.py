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

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test the public_repos method of the GithubOrgClient class."""
        json_payload = [
                {"name": "repo1", "license": "Nginx"},
                {"name": "repo2", "license": "Apache"}
        ]

        mock_get_json.return_value = json_payload
        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock:
            mock.return_value = "https://whatever.com/repos"
            client = GithubOrgClient('test_org')
            repos = client.public_repos()
            self.assertEqual(repos, [repo["name"] for repo in json_payload])
            mock_get_json.assert_called_once_with("https://whatever.com/repos")
            mock.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test the has_license method of the GithubOrgClient class."""
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
