import os
from utils import run_cmd

# Set required environment variables
REPOSITORY = os.environ["REPOSITORY"] if "REPOSITORY" in os.environ else None
REPOSITORY_OWNER = os.environ["REPOSITORY_OWNER"] if "REPOSITORY_OWNER" in os.environ else None
PR_NUMBER = os.environ["PR_NUMBER"] if "PR_NUMBER" in os.environ else None
PR_BRANCH_NAME = os.environ["PR_BRANCH_NAME"] if "PR_BRANCH_NAME" in os.environ else None

# Set optional environment variables
APPLY_LABELS = os.environ["APPLY_LABELS"] if "APPLY_LABELS" in os.environ else None
CLOSE_PR = True if "CLOSE_PR" in os.environ else False

# Check required environment variables are set
REQUIRED_ENV_VARS = {
    "REPOSITORY": REPOSITORY,
    "REPOSITORY_OWNER": REPOSITORY_OWNER,
    "PR_NUMBER": PR_NUMBER,
    "PR_BRANCH_NAME": PR_BRANCH_NAME,
}

for VARNAME, VAR in REQUIRED_ENV_VARS.items():
    if VAR is None:
        raise ValueError(
            f"{VARNAME} must be set"
        )

PROJECT_NAME = REPOSITORY.split("/")[-1]

# Clone the parent repo
run_cmd([
    "git",
    "clone",
    f"https://github.com/{REPOSITORY}.git",
])

# Change working directory
os.chdir(PROJECT_NAME)

# Add fork as remote
run_cmd([
    "git",
    "remote",
    "add",
    "fork",
    f"https://github.com/{REPOSITORY_OWNER}/{PROJECT_NAME}.git",
])

# Create a new branch
run_cmd([
    "git",
    "checkout",
    "-b",
    f"test-this-pr/{PR_NUMBER}",
])

# Merge PR branch into new branch
run_cmd([
    "git",
    "merge",
    f"fork/{PR_BRANCH_NAME}",
])

# Push new branch to parent repo
run_cmd([
    "git",
    "push",
    "origin",
    f"test-this-pr/{PR_NUMBER}",
])
