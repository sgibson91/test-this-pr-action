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

# API URL, default header and branch ref
API_URL = "https://api.github.com"
HEADER = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"token {ACCESS_TOKEN}",
}
BRANCH_REF = f"heads/test-this-pr/{PR_NUMBER}"

# See if BRANCH_REF already exists
match_ref_url = f"{API_URL}/repos/{REPOSITORY}/git/matching-refs/{BRANCH_REF}"
match_resp = get_request(match_ref_url, headers=HEADER, output="json")

# Fetch merge ref
merge_ref_url = f"{API_URL}/repos/{REPOSITORY}/git/ref/pull/{PR_NUMBER}/merge"
merge_resp = get_request(merge_ref_url, headers=HEADER, output="json")

if len(match_resp) > 0:
    # BRANCH_REF already exists, so we should update the ref
    branch_ref_url = f"{API_URL}/repos/{REPOSITORY}/git/refs/{BRANCH_REF}"
    body = {"sha": merge_resp["object"]["sha"], "force": True}
else:
    # BRANCH_REF does not exist, so we should create the ref
    branch_ref_url = f"{API_URL}/repos/{REPOSITORY}/git/refs"
    body = {"ref": f"refs/{BRANCH_REF}", "sha": merge_resp["object"]["sha"]}

post_request(branch_ref_url, headers=HEADER, json=body)

# Create a comment on the PR
issue_url = f"{API_URL}/repos/{REPOSITORY}/issues/{PR_NUMBER}/comments"
body = {
    "body": f"""
This Pull Request is now being tested :tada: See the test progress in [GitHub Actions](https://github.com/{REPOSITORY}/actions?query=branch%3Atest-this-pr%2F{PR_NUMBER}).
"""
}
post_request(issue_url, headers=HEADER, json=body)
