# Test this PR! - Docker-based Action

[![CI Tests](https://github.com/sgibson91/test-this-pr-action/actions/workflows/ci.yml/badge.svg)](https://github.com/sgibson91/test-this-pr-action/actions/workflows/ci.yml) [![pre-commit.ci status](https://results.pre-commit.ci/badge/github/sgibson91/test-this-pr-action/main.svg)](https://results.pre-commit.ci/latest/github/sgibson91/test-this-pr-action/main)

The fork --> develop --> open pull request workflow is a popular one across large software projects.
However if you have tests that require secrets, such as deploying to staging environments before production, this workflow can be a hindrance when managing that workflow through GitHub Actions, since the runner doesn't automatically grant access to repository secrets.

This repository is a Docker-based GitHub Action that will push the changes of a pull request opened from a fork into a new branch in the parent repo so test workflows that require secrets can be executed.

You will need to create a GitHub access token with enough permissions to write to the parent repo and save this as a repository secret.
If the parent repo is public, `public_repo` should be enough.

## Inputs

| Input variable | Description | Required? | Default value |
| :--- | :--- | :--- | :--- |
| `access_token` | A GitHub token with read/write access to the parent repository | Yes |  |
| `repository` | The name of the parent repository in the form `owner/project` | No | `${{ github.repository }}` |
| `pr_number` | The number of the Pull Request to be tested | No | `${{ github.event.issue.number }}` |

## Example Usage

The below example demonstrates how to trigger the GitHub Action by leaving a comment containing `/test-this-pr` on a pull request, providing the comment author has appropriate permissions on the parent repository.

**NOTE: These permissions are provided as an _example only_ and users should carefully read the [GitHub documentation](https://docs.github.com/en/graphql/reference/enums#commentauthorassociation) before deciding which roles to use.**

```yaml
name: Move forked-PR into parent repo for testing

on:
  issue_comment:
    types: [created]

jobs:
  test-this-pr:
    runs-on: ubuntu-latest
    if: |
      # Check this issue is a pull request
      (github.event.issue.pull_request != null) &&
      # Check the comment contains the trigger string
      contains(github.event.comment.body, '/test-this-pr') &&
      # Check the comment author has appropriate permissions
      contains(
        github.event.comment.author_association,
        ['OWNER', 'COLLABORATOR', 'MEMBER']
      )

    steps:
      - uses: sgibson91/test-this-pr-action@main
        with:
          access_token: ${{ secrets.ACCESS_TOKEN }}
```
