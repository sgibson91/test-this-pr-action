import os
from utils import run_cmd
from loguru import logger
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

logger.info("Checking environment variables...")
for VARNAME, VAR in REQUIRED_ENV_VARS.items():
    if VAR is None:
        logger.error("Unset environment variable!")
        raise ValueError(f"{VARNAME} must be set")
logger.info("Environment variables all good!")

# Set repository name
REPO_NAME = REPOSITORY.split("/")[-1]

# Clone the parent repo
logger.info(f"Cloning parent repository: {REPOSITORY}")
_ = run_cmd(
    [
        "git",
        "clone",
        f"https://{ACCESS_TOKEN}:x-oauth-basic@github.com/{REPOSITORY}.git",
    ]
)

# Change working directory
logger.info(f"Changing into dir: {REPO_NAME}")
os.chdir(REPO_NAME)

# Set remote URL to use credentials
logger.info("Updating remote to use credentials when pushing...")
_ = run_cmd(
    [
        "git",
        "remote",
        "set-url",
        "origin",
        f"https://{ACCESS_TOKEN}:x-oauth-basic@github.com/{REPOSITORY}.git",
    ]
)

# Fetch the existing merge ref and create a new local branch
logger.info(
    f"Fetching details for PR #{PR_NUMBER} and adding to branch test-this-pr/{PR_NUMBER}"
)
_ = run_cmd(
    ["git", "fetch", "origin", f"pull/{PR_NUMBER}/merge:test-this-pr/{PR_NUMBER}"]
)

# Push new branch to parent repo
logger.info(f"Force pushing branch: test-this-pr/{PR_NUMBER}")
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
logger.info(f"Adding comment to PR #{PR_NUMBER}")
api.issues.create_comment(
    REPOSITORY.split("/")[0],
    REPOSITORY.split("/")[-1],
    PR_NUMBER,
    body=f"""
This Pull Request is now being tested :tada: See the test progress in [GitHub Actions](https://github.com/{REPOSITORY}/actions?query=branch%3Atest-this-pr%2F{PR_NUMBER}).
""",
)
