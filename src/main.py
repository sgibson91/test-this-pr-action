import os
from utils import run_cmd
from ghapi.all import GhApi
from ghapi.actions import github_token

# Set required environment variables
ACCESS_TOKEN = (
    github_token()
    if "INPUT_ACCESS-TOKEN" not in os.environ
    else os.environ["INPUT_ACCESS-TOKEN"]
)
REPOSITORY = (
    os.environ["INPUT_REPOSITORY"] if "INPUT_REPOSITORY" in os.environ else None
)
PR_NUMBER = os.environ["INPUT_PR-NUMBER"] if "INPUT_PR-NUMBER" in os.environ else None

# Check required environment variables are set
REQUIRED_ENV_VARS = {
    "ACCESS_TOKEN": ACCESS_TOKEN,
    "REPOSITORY": REPOSITORY,
    "PR_NUMBER": PR_NUMBER,
}

for VARNAME, VAR in REQUIRED_ENV_VARS.items():
    if VAR is None:
        raise ValueError(f"{VARNAME} must be set")

# Set repository name
REPO_NAME = REPOSITORY.split("/")[-1]

# Clone the parent repo
_ = run_cmd(
    [
        "git",
        "clone",
        f"https://{ACCESS_TOKEN}:x-oauth-basic@github.com/{REPOSITORY}.git",
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
api = GhApi(token=ACCESS_TOKEN)

# Add comment to the old PR
api.issues.create_comment(
    REPOSITORY.split("/")[0],
    REPOSITORY.split("/")[-1],
    PR_NUMBER,
    body=f"""
This Pull Request is now being tested :tada: See the test progress in [GitHub Actions](https://github.com/{REPOSITORY}/actions?query=branch%3Atest-this-pr%2F{PR_NUMBER}).
""",
)
