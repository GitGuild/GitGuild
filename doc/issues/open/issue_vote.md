# Vote on an issue using XP

### commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| vote | issue_id, y/n | Add vote transaction on the given issue. |

### tests

| Name | Assertions | Description |
|------|------------|-------------|
| vote_y | yes vote entered against real issue | Create a valid issue then vote on it. |
| vote_n | no vote entered against real issue | Create a valid issue then vote on it. |
| vote_no_issue | warn, no action | vote entered against invalid issue |

