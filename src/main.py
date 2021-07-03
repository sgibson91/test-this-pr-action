import os

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
