# Contribute to a ledger using only XP

### commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| commit | all, message, submit | Also merge contributions and any other local changes to the 'voting' branch. |

### tests

| Name | Assertions | Description |
|------|------------|-------------|
| commit_good | commit to user branch made, merge commit from user to voting branch made | Create a valid contribution then commit it. |
| commit_bad_contribution | warn, no action | If contribution is not correctly formed, do not allow commit. |
