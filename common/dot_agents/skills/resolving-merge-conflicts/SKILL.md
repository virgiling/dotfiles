---
name: resolving-merge-conflicts
description: Resolve an in-progress Git merge or rebase conflict while preserving the intended changes on both sides.
---

1. Inspect status, operation state, conflicting files, and relevant commit history. Preserve unrelated staged and unstaged work.
2. Understand both changes and resolve hunks against the requested integration goal. If intentions are incompatible, explain the trade-off and ask only for the decision that blocks a correct resolution.
3. Run the repository's relevant checks and inspect the final diff for conflict markers or accidental loss of either change.
4. Stage only the resolved files when appropriate. Continue or commit the merge/rebase only when completing the operation is authorized; otherwise report that the files are resolved and what remains. Do not stage unrelated files, abort, or rewrite history without authorization.
