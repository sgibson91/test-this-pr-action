import os
import json
from utils import run_cmd
from ghapi.all import GhApi
from ghapi.actions import github_token

# Set required environment variables
REPOSITORY = (
    os.environ["INPUT_REPOSITORY"] if "INPUT_REPOSITORY" in os.environ else None
)
GITHUB_CONTEXT = (
    json.loads(os.environ["INPUT_GITHUB-CONTEXT"])
    if "INPUT_GITHUB-CONTEXT" in os.environ
    else None
)
GITHUB_TOKEN = (
    github_token()
    if "INPUT_GITHUB-TOKEN" not in os.environ
    else os.environ["INPUT_GITHUB-TOKEN"]
)
AUTHOR_NAME = (
    os.environ["INPUT_AUTHOR-NAME"] if "INPUT_AUTHOR-NAME" in os.environ else None
)
AUTHOR_EMAIL = (
    os.environ["INPUT_AUTHOR-EMAIL"] if "INPUT_AUTHOR-EMAIL" in os.environ else None
)

# Check required environment variables are set
REQUIRED_ENV_VARS = {
    "REPOSITORY": REPOSITORY,
    "GITHUB_CONTEXT": GITHUB_CONTEXT,
    "GITHUB_TOKEN": GITHUB_TOKEN,
    "AUTHOR_NAME": AUTHOR_NAME,
    "AUTHOR_EMAIL": AUTHOR_EMAIL,
}

for VARNAME, VAR in REQUIRED_ENV_VARS.items():
    if VAR is None:
        raise ValueError(f"{VARNAME} must be set")

# Initialise GhApi
api = GhApi(token=GITHUB_TOKEN)

# Set repository name
REPO_NAME = REPOSITORY.split("/")[-1]

# Set Pull Request number
PR_NUMBER = GITHUB_CONTEXT["issue"]["number"]

# Get Pull Request info
pr_info = api.pulls.get(REPOSITORY.split("/")[0], REPOSITORY.split("/")[-1], PR_NUMBER)

# Set fork owner
FORK_OWNER = pr_info.head.user.login

# Set Pull Request branch name
PR_BRANCH_NAME = pr_info.head.ref

# Set git config
_ = run_cmd(["git", "config", "user.name", AUTHOR_NAME])
_ = run_cmd(["git", "config", "user.email", AUTHOR_EMAIL])

# Clone the parent repo
_ = run_cmd(
    [
        "git",
        "clone",
        f"https://github.com/{REPOSITORY}.git",
    ]
)

# Change working directory
os.chdir(REPO_NAME)

# Add fork as remote
_ = run_cmd(
    [
        "git",
        "remote",
        "add",
        "fork",
        f"https://github.com/{FORK_OWNER}/{REPO_NAME}.git",
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

# Add comment to the old PR
api.issues.create_comment(
    REPOSITORY.split("/")[0],
    REPOSITORY.split("/")[-1],
    PR_NUMBER,
    body=f"This Pull Request is now being tested on the following branch: https://github.com/binderhub-test-org/pr-test/tree/test-this-pr/{PR_NUMBER}",
)
