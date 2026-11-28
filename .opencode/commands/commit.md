---
description: Review the diff, commit project changes with $ARGUMENTS, then rebase on main
---

Review the current project diff: run `git status` and `git diff`, and summarize what is changing. If the diff is empty, stop and report that there is nothing to commit.

Then stage the project changes and commit them with this exact message: $ARGUMENTS

Finally run `git pull --rebase origin main`. Report the commit hash and the result of the rebase.
