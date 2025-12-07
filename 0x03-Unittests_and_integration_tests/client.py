#!/usr/bin/env python3
"""
GithubOrgClient for fetching organization info and repositories from GitHub API.
"""

from typing import List, Dict
from utils import get_json, memoize


class GithubOrgClient:
    """Client to interact with GitHub organization endpoints."""

    ORG_URL = "https://api.github.com/orgs/{}"

    def __init__(self, org_name: str) -> None:
        self.org_name = org_name

    def org(self) -> Dict:
        """Return organization info as a dictionary."""
        return get_json(self.ORG_URL.format(self.org_name))

    @property
    def _public_repos_url(self) -> str:
        """Return the URL for public repositories."""
        return self.org().get("repos_url", "")

    def public_repos(self) -> List[str]:
        """Return a list of public repository names."""
        repos_info = get_json(self._public_repos_url)
        return [repo.get("name") for repo in repos_info]

    def has_license(self, repo: Dict, license_key: str) -> bool:
        """Check if a repository has the specified license."""
        return repo.get("license", {}).get("key") == license_key
