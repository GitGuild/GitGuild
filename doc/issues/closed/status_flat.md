# Get status of Guild using CII standards.

### commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| status | username, email | Check the status of the current guild, relative to the user given (default to current user) |

### tests

| Name | Assertions | Description |
|------|------------|-------------|
| status_empty | warn, suggest init | Attempt to get status of non-guild directory. |
| status | guild status and user status returned | Attempt to get status of good guild directory. |
| status_username | guild status and (another) user status returned | Attempt to get status of good guild directory using another username. |
