# gitguild

Guild-like governance for a git repository, using PGP identities.

IRC: #gitguild on freenode (see https://freenode.net/kb/answer/chat)

## Install

##### Try it out

Since this version of gitguild is a bourne shell script, it should be runnable as a standalone program on linux based systems. Macs and windows machines will definitely work with some work on the prerequisites.

##### Permanent

Installing in the specific location shown below is a more permanent and full featured method, providing transaction templates and a subscription to changes in the core.

```
mkdir -r $HOME/gitguild
git clone https://github.com/isysd/gitguild-cli $HOME/gitguild/gitguild
ln -sf $HOME/gitguild/gitguild /usr/bin/gitguild # or similar in PATH location
gitguild setup --gitolite
```

### Configure your user

This should happen during the above setup phase, or the first time gitguild is run. Gitguild has high expectations for the local git configuration, and may ask for some settings to be filled in.

```
WARNING: Git user.name not configured.

Please enter your git name followed by [ENTER]
```

You may also see some guessing or generation helpers. Just walk through it until it stops bothering you for more configuration.

```
guessing
Detected one or more keys matching your name or email.
The one you want is probably among these.
4E4FBA61 5C3586F6

Please enter your git signingkey followed by [ENTER]
```

Assuming you satisfy the script's prerequisites, it will no longer ask you these questions.

### System File Structure

| File | Directory | Description |
|------|-----------|-------------|
| *    | ~/gitguild | The default guild installation directory. Where repos are cloned for local work. |
| *    | ~/gitguild/\<username\> | Your personal guild's local clone. |
| *    | ~/gitguild/gitguild | Your clone of the gitguild source w/ templates & ledger. |
| *    | ~/repositories | The gitolite server repository data dir. DO NOT TOUCH! |

By default, all guilds are installed in `~/gitguild`, and your personal one will be in `~/gitguild/<username>`. It is likely that there will also be a local clone of this repo at `~/gitguild/gitguild`.

## Your Guild

Upon installation, a personal guild is created for you at `~/gitguild/<username>`. This is your personal blockchain, accounting, and file storage area. You can chose to share it with select people securely using ssh and gpg authentication.

This sharing will be important as your identity guild is also a permanent record of reference for your perspective on various balances, transactions and contracts.

##### Gitolite Configuration

Each guild is intended to be hosted on a [gitolite](http://gitolite.com/) server. In fact, one should have been installed locally during setup. Gitolite was chosen largely due to it's simple and in-repository configuration system, including permissions and authorisation.

For the most part these files should be automatically managed and you should not change them.

| File | Path from Repo | Description |
|------|-----------|-------------|
| gitolite.conf | /conf/ | The guild's gitolite configuration file. Sets permissions for all users and repositories. |
| *.pub | /keydir/ | The guild's member's public ssh keys. For gitolite authentication. |

##### (Mostly) Standard Documents

The goal of this first release of gitguild is to reach open source developers. Conversion of existing projects is a high priority, and so we've stayed as close to "standards" of open source development as possible. The [GNU standards](https://www.gnu.org/prep/standards/standards.html) were inspirational but not strictly followed.

| File | Path from Repo | Description |
|------|-----------|-------------|
| AUTHORS | / | The guild's member registry. All members must register here. |
| VERSION | / | The guild's version. Differ from gitguild software version. |
| CHANGELOG.md | / | A log of material changes. |
| CONTRIBUTING.md | / | Entry document to legal terms of participation and contribution. Any/all others should link from here. |

##### Unique Guild Documents

| File | Path from Repo | Description |
|------|-----------|-------------|
| GUILD | / | The guild's description file. Highest level summary data. |
| * | /ledger/ | The guild's accounting and voting records. (ledger-cli data) |
| * | /template/ | The guild's transaction templates. (patch files) |

## Ledger Entries

__This section is still planned...__

## CLI

This program is a command line suppliment to git. More effort was put into the help menus than this documentation, so far. ;)

```
	gitguild           	A helpful blockchain in a script.

	Usage:
		gitguild user	Manage your gitguild user.
		gitguild tx	    build and check transactions.
		gitguild push	git push with extra checks and remotes.
		gitguild setup	Install pre-requisites and configure gitguild.
		gitguild template	Create and list tx templates.
		gitguild help		Show the general help.
		gitguild version	Show the program version.

	Options:
		gitguild <cmd> -h	Show command help details.
```
