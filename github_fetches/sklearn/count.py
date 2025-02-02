import json
from pathlib import Path


def open_json(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


useless = "why-is-my-pull-request-not-getting-any-attention."

issues_path = Path("issues")
issue_num_to_data = {}
for path in issues_path.glob("*.json"):
    issues_batch = open_json(path)
    for issue_num, issue in issues_batch.items():
        issue["body_links"] = [
            link for link in issue["body_links"] if not link.endswith(useless)
        ]
    issue_num_to_data.update(issues_batch)

num_issues_with_links = sum(
    bool(issue["body_links"] + issue["comment_links"])
    for issue_num, issue in issue_num_to_data.items()
)
print(num_issues_with_links / len(issue_num_to_data))
