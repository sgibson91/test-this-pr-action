# Test this PR!

[![CI Tests](https://github.com/sgibson91/test-this-pr-action/actions/workflows/ci.yml/badge.svg)](https://github.com/sgibson91/test-this-pr-action/actions/workflows/ci.yml)

A GitHub Action to move a Pull Request from a fork into the parent repo so test workflows that require secrets can be executed.

## Inputs

### `repository`

### `repository-owner`

### `pr-number`

### `pr-branch-name`

### `github-token`

### `apply-labels`

## Example Usage

```yaml
name: Move forked-PR into parent repo for testing

on: [issue_comment]

jobs:
  test-this-pr:
    if: |
      (github.event.issue.pull_request != null) &&
      contains(github.event.comment.body, '/test-this-pr') &&
      (
          (github.event.issue.author_association == 'OWNER') ||
            (github.event.issue.author_association == 'COLLABORATOR') ||
            (github.event.issue.author_association == 'CONTRIBUTOR') ||
            (github.event.issue.author_association == 'MEMBER')
      )

    runs-on: ubuntu-latest

    steps:
      - uses: sgibson91/test-this-pr-action@master
        with:
          repository: ${{ github.repository }}
          repository-owner: ${{ github.event.pull_request.head.repo.owner.login }}
          pr-number: ${{ github.event.number }}
          pr-branch-name: ${{ github.head_ref }}
          github-token: ${{ secrets.GITHUB_TOKEN }}
```
