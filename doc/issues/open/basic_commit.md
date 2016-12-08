# Commit Guild without ledger

### commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| commit | all, message | Prepare CHANGELOG.md, commit message, etc., and then run git commit, signing with GPG |

### tests

| Name | Assertions | Description |
|------|------------|-------------|
| commit_empty | warning, suggest git add | Attempt to commit in an unchanged branch. |
| commit | Commit signed and created with all files prepared. | Attempt to commit in a changed branch. |
| commit_bad_status | warning, give status message | Attempt to commit in a branch returning a bad status. |
