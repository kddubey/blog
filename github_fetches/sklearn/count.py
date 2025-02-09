from collections import defaultdict
import json
from pathlib import Path

import seaborn as sns

sns.set_theme(style="darkgrid")


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

issue_num_to_links: dict[str, list[str]] = {
    issue_num: issue["body_links"] + issue["comment_links"]
    for issue_num, issue in issue_num_to_data.items()
    if issue["body_links"] + issue["comment_links"]
}
issue_num_to_pages = {}
for issue_num, links in issue_num_to_links.items():
    processed = {link.split("/")[-1].split("#")[0] for link in links}
    pages = {link for link in processed if link.endswith(".html")}
    if pages:
        issue_num_to_pages[issue_num] = pages

page_to_issue_nums = defaultdict(set)
for issue_num, pages in issue_num_to_pages.items():
    for page in pages:
        page_to_issue_nums[page].add(issue_num)
page_to_issue_nums = sorted(
    page_to_issue_nums.items(), key=lambda x: len(x[1]), reverse=True
)
num_issues_per_page = [len(issue_nums) for _, issue_nums in page_to_issue_nums]

num_issues_per_page = num_issues_per_page[2:]
# The first two pages are really basic and shouldn't be counted I think:
# contributing.html
# develop.html

sns.lineplot(x=range(len(num_issues_per_page)), y=num_issues_per_page)
