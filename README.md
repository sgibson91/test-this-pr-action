# Test this PR! - Docker-based Action

[![CI Tests](https://github.com/sgibson91/test-this-pr-action/actions/workflows/ci.yml/badge.svg)](https://github.com/sgibson91/test-this-pr-action/actions/workflows/ci.yml)

The fork --> develop --> open pull request workflow is a popular one across large software projects.
However if you have tests that require secrets, such as deploying to staging environments before production, this workflow can be a hindrance when managing that workflow through GitHub Actions, since the runner doesn't automatically grant access to repository secrets.

This repository is a Docker-based GitHub Action that will push the changes of a pull request opened from a fork into a new branch in the parent repo so test workflows that require secrets can be executed.

## Inputs

| Input variable | Description | Required? | Default value |
| :--- | :--- | :--- | :--- |
| `repository` | The name of the parent repository in the form `owner/project` | No | `${{ github.repository }}` |
| `github-issue-context` | The context of the issue the trigger comment was left on (equivalent to a Pull Request to GitHub's API). From this context we can establish who owns the fork the PR originates from and the branch name. | No | `${{ github.event.issue }}` |
| `github-token` | A GitHub token with read/write access to the parent repository | No | `${{ github.token }}` |

## Example Usage

The below example demonstrates how to trigger the GitHub Action by leaving a comment containing `/test-this-pr` on a pull request, providing the comment author has appropriate permissions on the parent repository.

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
      (
        (github.event.issue.author_association == 'OWNER') ||
        (github.event.issue.author_association == 'COLLABORATOR') ||
        (github.event.issue.author_association == 'CONTRIBUTOR') ||
        (github.event.issue.author_association == 'MEMBER')
      )

    steps:
      - uses: sgibson91/test-this-pr-action@main
```
