import os
from utils import get_request, post_request


# Set required environment variables
ACCESS_TOKEN = (
    os.environ["INPUT_ACCESS_TOKEN"] if "INPUT_ACCESS_TOKEN" in os.environ else None
)
REPOSITORY = (
    os.environ["INPUT_REPOSITORY"] if "INPUT_REPOSITORY" in os.environ else None
)
PR_NUMBER = os.environ["INPUT_PR_NUMBER"] if "INPUT_PR_NUMBER" in os.environ else None

# Check required environment variables are set
REQUIRED_ENV_VARS = {
    "INPUT_ACCESS_TOKEN": ACCESS_TOKEN,
    "INPUT_REPOSITORY": REPOSITORY,
    "INPUT_PR_NUMBER": PR_NUMBER,
}

for VARNAME, VAR in REQUIRED_ENV_VARS.items():
    if VAR is None:
        raise ValueError(f"{VARNAME} must be set!")

# API URL and default header
API_URL = "https://api.github.com"
HEADER = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {ACCESS_TOKEN}",
}

# Fetch merge ref
merge_ref_url = f"{API_URL}/repos/{REPOSITORY}/git/ref/pull/{PR_NUMBER}/merge"
resp = get_request(merge_ref_url, headers=HEADER, output="json")

# Create new branch ref
new_branch_ref_url = f"{API_URL}/repos/{REPOSITORY}/git/refs"
body = {"ref": f"refs/heads/test-this-pr/{PR_NUMBER}", "sha": resp["object"]["sha"]}
post_request(new_branch_ref_url, headers=HEADER, json=body)

# Create a comment on the PR
issue_url = f"{API_URL}/repos/{REPOSITORY}/issues/{PR_NUMBER}/comments"
body = {
    "body": f"""
This Pull Request is now being tested :tada: See the test progress in [GitHub Actions](https://github.com/{REPOSITORY}/actions?query=branch%3Atest-this-pr%2F{PR_NUMBER}).
"""
}
post_request(issue_url, headers=HEADER, json=body)
