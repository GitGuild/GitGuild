# Make and check file templates

### commands

| Command | Arguments | Description |
|---------|-----------|-------------|
| make_template | input_file | Create a template file out of a source file. For patching and validation of commits. |

### tests

| Name | Assertions | Description |
|------|------------|-------------|
| status_local_changes | local changes represent a valid commit, and are scored | Check the local changes against the guild's permitted templates. |


### Comments

##### isysd

The best way to manage these templates seems to be through diffs and patches. That is, each template represents a permittable diff profile. Each commit must match one of these profiles for the other members to recognize it as valid.

Another problem is metadata. The metadata will have to include at minimum the number of votes required to confirm a transaction. So far experimentation has been with json schemas for this metadata, but a custom unified template file structure is more efficient. Json is badly suited for a unified file structure as it doesn't preserve whitespace, newlines and other important data.
