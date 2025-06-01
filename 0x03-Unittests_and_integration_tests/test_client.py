#!/usr/bin/env python3
"""Unit and Integration tests for GithubOrgClient
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test GithubOrgClient.org returns correct value"""
        expected = {"login": org_name, "id": 123}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        self.assertEqual(result, expected)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test GithubOrgClient._public_repos_url"""
        mock_org.return_value = {"repos_url": "http://some_url.com"}
        client = GithubOrgClient("test")

        self.assertEqual(client._public_repos_url, "http://some_url.com")

    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """Test GithubOrgClient.public_repos"""
        mock_public_repos_url.return_value = "http://some_url.com"
        mock_get_json.return_value = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3"}
        ]

        client = GithubOrgClient("test")
        result = client.public_repos()
        self.assertEqual(result, ["repo1", "repo2", "repo3"])

        result_apache = client.public_repos(license="apache-2.0")
        self.assertEqual(result_apache, ["repo1"])

        mock_get_json.assert_called_once()
        mock_public_repos_url.assert_called_once()

    @parameterized.expand([
        ("repo_with_license", {"license": {"key": "my_license"}}, "my_license", True),
        ("repo_with_other_license", {"license": {"key": "other_license"}}, "my_license", False),
        ("repo_without_license", {}, "my_license", False)
    ])
    def test_has_license(self, _, repo, license_key, expected):
        """Test GithubOrgClient.has_license"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


@parameterized_class([
    {
        "org_payload": TEST_PAYLOAD["org_payload"],
        "repos_payload": TEST_PAYLOAD["repos_payload"],
        "expected_repos": TEST_PAYLOAD["expected_repos"],
        "apache2_repos": TEST_PAYLOAD["apache2_repos"],
    }
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    @classmethod
    def setUpClass(cls):
        """Set up mock for requests.get().json"""
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        # Configure mock to return different payloads based on URL
        def side_effect(url):
            if url.endswith("/orgs/google"):
                return MockResponse(cls.org_payload)
            elif url.endswith("/orgs/google/repos"):
                return MockResponse(cls.repos_payload)
            return MockResponse(None)

        mock_get.side_effect = lambda url: side_effect(url)

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test integration: public_repos"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test integration: public_repos with license filter"""
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )


class MockResponse:
    """Mock response object for requests.get().json()"""
    def __init__(self, payload):
        self._payload = payload

    def json(self):
        return self._payload
