# Test this PR! - Docker-based Action

[![CI Tests](https://github.com/sgibson91/test-this-pr-action/actions/workflows/ci.yml/badge.svg)](https://github.com/sgibson91/test-this-pr-action/actions/workflows/ci.yml)

The fork --> develop --> open pull request workflow is a popular one across large software projects.
However, if you have tests that require secrets, such as deploying to staging environments before production, this workflow can be a hindrance when managing that workflow through GitHub Actions, since the runner doesn't automatically grant access to repository secrets.

This repository is a Docker-based GitHub Action that will move a pull request opened from a fork into the parent repo so test workflows that require secrets can be executed.

Yes, we could use [`ok-to-test`](https://github.com/imjohnbo/ok-to-test) instead.
We found a lot of extra infrastructure was required to setup this action (e.g. a GitHub App) and we also wanted to take advantage of existing infrastructure that runs our staging deployment when a specific label is applied to an open pull request.

## Inputs

### `repository`

This is the name of the parent repository in the form `owner/project`.
It can be accessed during a workflow run with the `${{ github.repository }}` context.

### `fork-owner`

This is the account that holds the fork of the parent repository.
It can be accessed during a workflow run _triggered by a pull request event_ in the `${{ github.event.pull_request.head.repo.owner.login }}` context.
### `pr-number`

This is the number of the pull request that was opened from a fork.
It can be accessed during a workflow run _triggered by a pull request event_ in the `${{ github.event.number }}` context.

### `pr-branch-name`

This is the name of the branch in the fork from which the pull request originated.
It can be accessed during a workflow run _triggered by a pull request event_ using the `${{ github.head_ref }}` context.

### `github-token`

This is a GitHub token with read/write access to the parent repository.
During a workflow run `${{ secrets.GITHUB_TOKEN }}` should have the required permissions.

### `apply-labels`

This is an **optional** field that will apply labels to the new pull request, so long as those labels already exist in the repository.
This field accepts a _whitespace separated_ list of inputs, hence it will **fail if your label names also include whitespace**.

## Example Usage

The below example demonstrates how to trigger the GitHub Action by leaving a comment containing `/test-this-pr` on a pull request, providing the comment author has appropriate permissions on the parent repository.

```yaml
name: Move forked-PR into parent repo for testing

on: [issue_comment]

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
      - uses: sgibson91/test-this-pr-action@master
        with:
          repository: ${{ github.repository }}
          fork-owner: ${{ github.event.pull_request.head.repo.owner.login }}
          pr-number: ${{ github.event.number }}
          pr-branch-name: ${{ github.head_ref }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
          apply-labels: test-staging label-1 label-2 ...
```
