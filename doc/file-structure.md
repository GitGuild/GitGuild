# System File Structure

| Directory | File | Description |
|-----------|------|-------------|
| ~/gitguild | *    | The default guild installation directory. Where repos are cloned for local work. |
| ~/gitguild/<username\> | *    | Your personal guild's local clone. |
| ~/gitguild/gitguild | *    | Your clone of the gitguild source w/ templates & ledger. |
| ~/repositories | *    | The gitolite server repository data dir. DO NOT TOUCH! |

By default, all guilds are installed in `~/gitguild`, and your personal one will be in `~/gitguild/<username>`. It is likely that there will also be a local clone of this repo at `~/gitguild/gitguild`.

### Your Guild

Upon installation, a personal guild is created for you at `~/gitguild/<username>`. This is your personal blockchain, accounting, and file storage area. You can chose to share it with select people securely using ssh and gpg authentication.

This sharing will be important as your identity guild is also a permanent record of reference for your perspective on various balances, transactions and contracts.

##### Gitolite Configuration

Each guild is intended to be hosted on a [gitolite](http://gitolite.com/) server. In fact, one should have been installed locally during setup. Gitolite was chosen largely due to it's simple and in-repository configuration system, including permissions and authorisation.

For the most part these files should be automatically managed and you should not change them.

| Path from Repo | File | Description |
|-----------|------|-------------|
| /conf/ | gitolite.conf | The guild's gitolite configuration file. Sets permissions for all users and repositories. |
| /keydir/ | *.pub | The guild's member's public ssh keys. For gitolite authentication. |

##### (Mostly) Standard Documents

The goal of this first release of gitguild is to reach open source developers. Conversion of existing projects is a high priority, and so we've stayed as close to "standards" of open source development as possible. The [GNU standards](https://www.gnu.org/prep/standards/standards.html) were inspirational but not strictly followed.

| Path from Repo | File | Description |
|-----------|------|-------------|
| / | AUTHORS | The guild's member registry. All members must register here. |
| / | VERSION | The guild's version. Differ from gitguild software version. |
| / | CHANGELOG.md | A log of material changes. |
| / | CONTRIBUTING.md | Entry document to legal terms of participation and contribution. Any/all others should link from here. |

##### Unique Guild Documents

| Path from Repo | File | Description |
|-----------|------|-------------|
| / | GUILD | The guild's description file. Highest level summary data. |
| /ledger/ | * | The guild's accounting and voting records. (ledger-cli data) |
| /template/ | * | The guild's transaction templates. (patch files) |
