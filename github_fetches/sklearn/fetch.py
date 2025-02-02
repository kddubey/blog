import json
from math import ceil
import os
from typing import Any, TypeAlias, Union
import requests
import re
from tenacity import (
    after_log,
    before_sleep_log,
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
import logging
import sys

NestedDict: TypeAlias = dict[str, Union["NestedDict", Any]]

# GitHub API Credentials
GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
OWNER = "scikit-learn"
REPO = "scikit-learn"

# API Endpoints
ISSUES_API_URL = f"https://api.github.com/repos/{OWNER}/{REPO}/issues"
GRAPHQL_API_URL = "https://api.github.com/graphql"

# Regex pattern to find scikit-learn doc links
SKLEARN_DOCS_PATTERN = r"https?://scikit-learn\.org[^\s,)<>]*"

# Headers for authentication
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

# Setup logging to stdout
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()


def save_intermediate_results(data: dict, category: str, identifier: str) -> str:
    filename = os.path.join(category, f"{identifier}.json")
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"Saved to {filename}")
    return filename


def retry_default():
    return retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(requests.exceptions.RequestException),
        before_sleep=before_sleep_log(logger, logging.INFO),
        after=after_log(logger, logging.INFO),
        reraise=True,
    )


def extract_links(text: str | None) -> list[str]:
    return re.findall(SKLEARN_DOCS_PATTERN, text) if text else []


@retry_default()
def fetch_comments(
    comments_url: str, num_comments: int = 10, per_page: int = 10
) -> list[str]:
    """
    Fetch all comments for an issue's comments and extract scikit-learn documentation
    links.
    """
    links = []
    for page in range(1, num_comments + 1):
        params = {"per_page": per_page, "page": page}
        response = requests.get(comments_url, headers=HEADERS, params=params)
        if response.status_code != 200:
            break
        comments: list[dict] = response.json()
        for comment in comments:
            links.extend(extract_links(comment.get("body", "")))
    return links


@retry_default()
def fetch_issues(page: int, per_page: int = 10, state: str = "all") -> list[dict]:
    response = requests.get(
        ISSUES_API_URL,
        headers=HEADERS,
        params={"page": page, "per_page": per_page, "state": state},
    )
    if response.status_code != 200:
        logger.error(
            f"Page: {page}. Error fetching issues. "
            f"Status Code: {response.status_code}. Response: {response.text}"
        )
        response.raise_for_status()
    return response.json()


def save_issues(
    num_issues: int = 5_000, num_issues_per_page: int = 10, state: str = "all"
):
    """
    Fetch all issues from the repository and save their scikit-learn documentation
    links.
    """
    num_pages = ceil(num_issues // num_issues_per_page)
    for page in range(1, num_pages + 1):
        issues = fetch_issues(page, num_issues_per_page, state)
        if not issues:
            logger.error(f"Page: {page}. No issues found.")
            break
        issues_links = {}
        for issue in issues:
            issue_number = issue["number"]
            issue_links = extract_links(issue.get("body", ""))
            comment_links = fetch_comments(issue["comments_url"])
            issues_links[issue_number] = {
                "type": "issue",
                "title": issue["title"],
                "url": issue["html_url"],
                "body_links": issue_links,
                "comment_links": comment_links,
            }
        save_intermediate_results(issues_links, "issues", page)


@retry_default()
def save_discussions():
    """
    Fetch all discussions using the GitHub GraphQL API and save their scikit-learn
    documentation links.
    """
    cursor = None
    while True:
        query = f"""
        {{
            repository(owner: "{OWNER}", name: "{REPO}") {{
                discussions(first: 100{', after: "' + cursor + '"' if cursor else ''}) {{
                    pageInfo {{
                        endCursor
                        hasNextPage
                    }}
                    nodes {{
                        id
                        title
                        url
                        body
                        comments(first: 100) {{
                            nodes {{
                                body
                            }}
                        }}
                    }}
                }}
            }}
        }}
        """
        response = requests.post(
            GRAPHQL_API_URL, json={"query": query}, headers=HEADERS
        )
        if response.status_code != 200:
            logger.error(
                f"Error fetching discussions (Status Code: {response.status_code})"
            )
            break
        data: NestedDict = response.json()
        discussions_data = (
            data.get("data", {}).get("repository", {}).get("discussions", {})
        )

        discussions_links = {}
        discussions = discussions_data.get("nodes", [])
        for discussion in discussions:
            discussion_id = discussion["id"]
            body_links = extract_links(discussion["body"])
            nodes: list[dict] = discussion["comments"]["nodes"]
            comment_links = [
                extract_links(comment.get("body", "")) for comment in nodes
            ]
            discussions_links[discussion_id] = {
                "type": "discussion",
                "title": discussion["title"],
                "url": discussion["url"],
                "body_links": body_links,
                "comment_links": comment_links,
            }

        if not discussions_data.get("pageInfo", {}).get("hasNextPage"):
            logger.info("No more discussions found.")
            break

        cursor = discussions_data["pageInfo"].get("endCursor")
        save_intermediate_results(discussions_links, "discussions", cursor)


if __name__ == "__main__":
    save_issues()
