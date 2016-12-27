# Contribute to a ledger using only XP

### commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| contribute | XP | Add contribution transaction to the ledger with the given number of XP going to the current user. |

### tests

| Name | Assertions | Description |
|------|------------|-------------|
| init_ledger | (ledger, ledger/definitions.ledger, ledger/coa.ledger, ledger/changelog.ledger, ledger/checks.ledger) | initialize with ledger files |
| contribute | ledger file updated, status pass | success |
| contribute_bad | status fail, commit fail | Ensure that status and commit fail appropriately when an invalid contribution is in the ledger. |
