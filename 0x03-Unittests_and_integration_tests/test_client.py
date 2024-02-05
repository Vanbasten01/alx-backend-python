#!/usr/bin/env python3
"""This script tests the org method of the GithubOrgClient class."""

import unittest
from parameterized import parameterized, parameterized_class
from unittest.mock import patch, PropertyMock, Mock
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


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

@parameterized_class(('org_payload', 'repos_payload', 'expected_repos',
                     'apache2_repos'), TEST_PAYLOAD)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test cases for the GithubOrgClient class."""
    @classmethod
    def setUpClass(cls):
        """Set up the class for integration testing."""
        def side_effects(url):
            """Side effect function for requests.get mock."""
            mock_response = Mock()
            for payload in TEST_PAYLOAD:
                if url == payload[0]["repos_url"]:
                    repo = payload[1]
                    break
            mock_response.json.return_value = repo
            return mock_response
        cls.get_patcher = patch("requests.get", side_effect=side_effects)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Tear down the class after integration testing."""
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()
