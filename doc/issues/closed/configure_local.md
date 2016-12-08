# Configure local GitGuild settings

### commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| config | username, email, signingkey | Get the username, email and signingkey from git, or set them if empty. |

### tests

| Name | Assertions | Description |
|------|------------|-------------|
| config_fresh | prompted, keys set | When configuring for the first time, user should be prompted to fill in any missing git config settings. After that, values are returned. |
