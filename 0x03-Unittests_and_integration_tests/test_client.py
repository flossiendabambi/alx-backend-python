#!/usr/bin/env python3
"""Unit and integration tests for GithubOrgClient"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
import requests


# Fixtures used for integration tests
org_payload = {
    "login": "testorg",
    "repos_url": "https://api.github.com/orgs/testorg/repos"
}
repos_payload = [
    {"name": "repo1", "license": {"key": "apache-2.0"}},
    {"name": "repo2", "license": {"key": "mit"}},
    {"name": "repo3", "license": {"key": "apache-2.0"}},
]
expected_repos = ["repo1", "repo2", "repo3"]
apache2_repos = ["repo1", "repo3"]


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct payload"""
        expected = {"login": org_name}
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch("client.get_json")
    def test_public_repos_url(self, mock_get_json):
        """Test _public_repos_url property"""
        mock_get_json.return_value = {"repos_url": "http://test.com"}
        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://test.com"}
            client = GithubOrgClient("testorg")
            self.assertEqual(client._public_repos_url, "http://test.com")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns repo names"""
        mock_get_json.return_value = repos_payload
        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "http://test.com"
            client = GithubOrgClient("testorg")
            self.assertEqual(client.public_repos(), expected_repos)
            self.assertEqual(
                client.public_repos(license="apache-2.0"),
                apache2_repos
            )
            mock_get_json.assert_called_once()
            mock_url.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
        ({}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license returns correct result"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": org_payload,
        "repos_payload": repos_payload,
        "expected_repos": expected_repos,
        "apache2_repos": apache2_repos,
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests with patched requests.get"""

    @classmethod
    def setUpClass(cls):
        """Patch requests.get and set side_effect to return fixture data"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            if url == "https://api.github.com/orgs/testorg":
                return MockResponse(cls.org_payload)
            elif url == cls.org_payload["repos_url"]:
                return MockResponse(cls.repos_payload)
            return None

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Integration test for public_repos"""
        client = GithubOrgClient("testorg")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Integration test for public_repos with license filter"""
        client = GithubOrgClient("testorg")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


class MockResponse:
    """Mock response for requests.get"""
    def __init__(self, json_data):
        self._json_data = json_data

    def json(self):
        return self._json_data


if __name__ == '__main__':
    unittest.main()
