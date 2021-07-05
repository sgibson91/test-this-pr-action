import os
from utils import post_request, run_cmd

# Set required environment variables
REPOSITORY = (
    os.environ["INPUT_REPOSITORY"] if "INPUT_REPOSITORY" in os.environ else None
)
FORK_OWNER = (
    os.environ["INPUT_FORK_OWNER"] if "INPUT_FORK_OWNER" in os.environ else None
)
PR_NUMBER = os.environ["INPUT_PR_NUMBER"] if "INPUT_PR_NUMBER" in os.environ else None
PR_BRANCH_NAME = (
    os.environ["INPUT_PR_BRANCH_NAME"] if "InPUT_PR_BRANCH_NAME" in os.environ else None
)
GITHUB_TOKEN = (
    os.environ["INPUT_GITHUB_TOKEN"] if "INPUT_GITHUB_TOKEN" in os.environ else None
)

# Set optional environment variables
APPLY_LABELS = (
    os.environ["INPUT_APPLY_LABELS"] if "INPUT_APPLY_LABELS" in os.environ else None
)

# Check required environment variables are set
REQUIRED_ENV_VARS = {
    "REPOSITORY": REPOSITORY,
    "FORK_OWNER": FORK_OWNER,
    "PR_NUMBER": PR_NUMBER,
    "PR_BRANCH_NAME": PR_BRANCH_NAME,
    "GITHUB_TOKEN": GITHUB_TOKEN,
}

for VARNAME, VAR in REQUIRED_ENV_VARS.items():
    if VAR is None:
        raise ValueError(f"{VARNAME} must be set")

PROJECT_NAME = REPOSITORY.split("/")[-1]

# Clone the parent repo
_ = run_cmd(
    [
        "git",
        "clone",
        f"https://github.com/{REPOSITORY}.git",
    ]
)

# Change working directory
os.chdir(PROJECT_NAME)

# Add fork as remote
_ = run_cmd(
    [
        "git",
        "remote",
        "add",
        "fork",
        f"https://github.com/{FORK_OWNER}/{PROJECT_NAME}.git",
    ]
)

# Create a new branch
_ = run_cmd(
    [
        "git",
        "checkout",
        "-b",
        f"test-this-pr/{PR_NUMBER}",
    ]
)

# Fetch the fork
_ = run_cmd(
    [
        "git",
        "fetch",
        "fork",
    ]
)

# Merge PR branch into new branch
_ = run_cmd(
    [
        "git",
        "merge",
        f"fork/{PR_BRANCH_NAME}",
    ]
)

# Push new branch to parent repo
_ = run_cmd(
    [
        "git",
        "push",
        "origin",
        f"test-this-pr/{PR_NUMBER}",
    ]
)

# Get the default branch of the parent repo
# to set as base branch of Pull Request
result = run_cmd(
    [
        "git",
        "symbolic-ref",
        "refs/remotes/origin/HEAD",
    ]
)
base_branch = result["output"].split("/")[-1]

# Create Pull Request template
pr = {
    "title": f"Testing PR #{PR_NUMBER}",
    "body": f"This PR is a copy of PR #{PR_NUMBER} which came from a fork. Tests that require secrets can now be run on this PR.",
    "base": base_branch,
    "head": f"test-this-pr/{PR_NUMBER}",
}

# Create the Pull Request
resp = post_request(
    f"https://api.github.com/repos/{REPOSITORY}/pulls",
    headers={"Authorization": f"token {GITHUB_TOKEN}"},
    json=pr,
    return_json=True,
)

PR_URL = resp["html_url"]
PR_URL_API = resp["issue_url"]

# Add labels to the new PR
if APPLY_LABELS is not None:
    post_request(
        PR_URL_API + "/labels",
        headers={"Authorization": f"token {GITHUB_TOKEN}"},
        json={"labels": APPLY_LABELS.split(" ")},
    )

# Add comment to the old PR
post_request(
    f"https://api.github.com/repos/{REPOSITORY}/issues/{PR_NUMBER}/comments",
    headers={"Authorization": f"token {GITHUB_TOKEN}"},
    json={"body": f"This Pull Request is now being tested in {PR_URL}"},
)
