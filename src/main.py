import os
import json
from utils import run_cmd
from ghapi.all import GhApi
from ghapi.actions import github_token

# Set required environment variables
REPOSITORY = (
    os.environ["INPUT_REPOSITORY"] if "INPUT_REPOSITORY" in os.environ else None
)
PR_NUMBER = os.environ["INPUT_PR-NUMBER"] if "INPUT_PR-NUMBER" in os.environ else None
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
    "PR_NUMBER": PR_NUMBER,
    "GITHUB_TOKEN": GITHUB_TOKEN,
    "AUTHOR_NAME": AUTHOR_NAME,
    "AUTHOR_EMAIL": AUTHOR_EMAIL,
}

for VARNAME, VAR in REQUIRED_ENV_VARS.items():
    if VAR is None:
        raise ValueError(f"{VARNAME} must be set")

# Set repository name
REPO_NAME = REPOSITORY.split("/")[-1]

# Set git config
_ = run_cmd(["git", "config", "user.name", AUTHOR_NAME])
_ = run_cmd(["git", "config", "user.email", AUTHOR_EMAIL])

# Clone the parent repo
_ = run_cmd(
    [
        "git",
        "clone",
        f"https://{GITHUB_TOKEN}:x-oauth-basic@github.com/{REPOSITORY}.git",
    ]
)

# Change working directory
os.chdir(REPO_NAME)

# Fetch the existing merge ref and create a new local branch
_ = run_cmd(
    ["git", "fetch", "origin", f"pull/{PR_NUMBER}/merge:test-this-pr/{PR_NUMBER}"]
)

# Push new branch to parent repo
_ = run_cmd(
    [
        "git",
        "push",
        "--force",
        "origin",
        f"test-this-pr/{PR_NUMBER}",
    ]
)

# Initialise GhApi
api = GhApi(token=GITHUB_TOKEN)

# Add comment to the old PR
api.issues.create_comment(
    REPOSITORY.split("/")[0],
    REPOSITORY.split("/")[-1],
    PR_NUMBER,
    body=f"This Pull Request is now being tested on the following branch: https://github.com/binderhub-test-org/pr-test/tree/test-this-pr/{PR_NUMBER}",
)
