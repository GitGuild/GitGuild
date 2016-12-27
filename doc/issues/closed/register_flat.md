# Register for a Guild using CII standards.

### commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| register | username, fingerprint, email | Add a user to the AUTHORS file. |

### tests

| Name | Assertions | Description |
|------|------------|-------------|
| register | user added to AUTHORS | success |
| register_duplicate_username | warning, no action | error |
| register_duplicate_email | warning, no action | error |
| register_duplicate_fingerprint | warning, no action | error |
