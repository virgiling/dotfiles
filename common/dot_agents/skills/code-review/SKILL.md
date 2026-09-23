---
name: code-review
description: Review a diff, branch, PR, or uncommitted changes for correctness and compliance with the stated requirements. Use for a requested code review, not automatically after every edit.
---

# Review changes

## Establish scope

Use the user's requested base and working-tree scope. Inspect repository status first.
- Branch review: resolve the base and review `git diff <base>...HEAD` plus relevant commits.
- WIP review: include `git diff` and `git diff --cached`, and inspect relevant untracked files separately. Do not silently omit uncommitted work.
- If scope is genuinely ambiguous, state a reasonable assumption or ask a focused question.

Read the requirements from the request, supplied issue/PR, or local spec. Use the repository's existing tracker integration if available; no setup skill is a prerequisite. If no spec exists, review against the stated intent and identify the limitation.

## Review two concerns

1. **Correctness and requirements:** changed behavior, regressions, security, edge cases, missing requirements, and unsupported scope expansion.
2. **Repository standards:** concrete documented constraints not already covered by deterministic tooling. Do not impose generic line counts, pattern preferences, or coverage quotas.

Follow changed code into callers or tests only as needed to substantiate a finding. For substantial independent concerns, use fresh-context reviewers if supported; otherwise perform the passes directly and do not claim independent review.

## Report

List actionable findings by severity with file/line references, the triggering condition, impact, and evidence. Separate defects from optional suggestions. A clean review is valid; do not invent findings to fill a quota.

Summarize checks actually performed and unresolved gaps. Do not edit code or publish review comments unless requested.
