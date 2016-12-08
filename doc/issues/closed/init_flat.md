# Initialize Guild using CII standards.

### commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| init    | license, register | Create the required guild file structure, inspired by general git standards enumerated by CII. (CONTRIBUTING.md, LICENSE, AUTHORS, CHANGELOG.md, doc, etc.) |

### tests

| Name | Assertions | Description |
|------|------------|-------------|
| init_empty | (LICENSE, AUTHORS, CHANGELOG.md, CONTRIBUTING.md, doc) exists | Guild files created from empty directory. |
| init_full | warning, no action | Attempt to initialize over an existing guild. |
