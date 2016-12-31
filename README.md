# gitguild

Guild governance for a git repository, using PGP identities.

 + Issue digital value tokens
 + Create, sign, and enforce contracts
 + Participate in projects in a democratic, decentralized manner

## Try it out

Just download and run `gitguild`.

Since this version is a bourne shell script, it should be runnable as a standalone program on most linux and MacOS systems. More work is necessary to make the script Windows compatible, but there are no barriers.

As a command line supplement to git, the help menus are comprehensive.

```
	gitguild           	A helpful blockchain in a script.

	Usage:
		gitguild user	Manage your gitguild user.
		gitguild tx	    build and check transactions.
		gitguild ledger	Perform gitguild-related ledger actions.
		gitguild clone	<guild>	(<remote>) Clone a guild from optional remote.
		gitguild push	git push with extra checks and remotes.
		gitguild fork	<remote>	Fork a guild with one or more remotes.
		gitguild setup-repo	Setup remotes and hooks in current git repo.
		gitguild template	Create and list tx templates.
		gitguild help		Show the general help.
		gitguild version	Show the program version.

	Options:
		gitguild <cmd> -h	Show command help details.
```

## Install

Installing in the specific location shown below is a more permanent and full featured method, providing transaction templates and a subscription to changes in the core.

```
mkdir $HOME/gitguild
git clone https://github.com/isysd/gitguild-cli $HOME/gitguild/gitguild
cd $HOME/gitguild/gitguild
./configure # will ask for password for new 'git' user
make install
```

__*System restart will be required at this point!*__

The install process created a new 'git' user and group on your system, and additionally changed the hostname. These require a system reboot before taking affect, and the next step will not work without it.

After your reboot, you can create your personal guild, if you haven't done so on a previous occasion.

```
make personal
```

For more details on the output of this full install process, read `./doc/file-structure.md`.

##### Pre-requisites

The following programs are required to be installed on the system prior to running gitguild. Note that git and ledger-cli must have recent versions! Depending on your system, the configure and make commands may help you install these. (Ubuntu only, for now)

 + [git](https://git-scm.com/downloads) 2.0+
 + [Ledger-cli](http://ledger-cli.org/download.html) 3.0+ (2.x is not good enough!)
 + [GnuPG](https://gnupg.org/download/index.html)

### Configure your user

This should happen during the `./configure` step of the above setup phase, or the first time gitguild is run. Gitguild has high expectations for the local git configuration, and may ask for some settings to be filled in.

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

Assuming you satisfy the script's prerequisites, it will no longer ask you these questions. It may, however, warn you that you are not in the AUTHORS file. This is expected until you register for a specific guild.

##### Github Integration

Thanks to [ok.sh](https://github.com/whiteinge/ok.sh), gitguild can also integrate with [github](https://github.com) seamlessly. Just run `make install` with `USE_GITHUB=true` (the default), and it will add your github credentials to `~/.netrc` as described in [ok.sh setup](https://github.com/whiteinge/ok.sh#setup).

Note that gitguild asks for the following permissions for your token:

+ [x] repo (three boxes)
+ [ ] admin:repo_hook
+ [ ] admin:org_hook
+ [ ] user:email
+ [ ] read:public_key
+ [ ] read:gpg_key

The unchecked ones are not currently used, but planned for the future. Unlisted ones will probably never be needed by this program.

If you wish to disable github integration, run `configure` and `make install` with argument `USE_GITHUB=false`.

## Additional Resources

Guilds keep all documentatation, issues, and other project-relevant information inside the repository. There are a number of detailed documents in the top level of this docs directory that are a good place to start.

### General

 + docs/faq.md

### Technical

 + docs/roadmap.md
 + docs/file-structure.md
 + docs/templates.md
 + docs/ledger.md

## Help

Make an issue on github, or in the `docs/issues` directory, if you are a member.

Join us on IRC chat channel `#gitguild` on freenode (see https://freenode.net/kb/answer/chat).

## License

To quote the Linux Foundation's [Core Infrastructure Initiative](https://github.com/linuxfoundation/cii-best-practices-badge), from whom we borrowed so much:

All material is released under the [MIT license](./LICENSE).
All material that is not executable, including all text when not executed,
is also released under the
[Creative Commons Attribution 3.0 International (CC BY 3.0) license](https://creativecommons.org/licenses/by/3.0/) or later.
In SPDX terms, everything here is licensed under MIT;
if it's not executable, including the text when extracted from code, it's
"(MIT OR CC-BY-3.0+)".

See CREDITS file for more on CII and other excellent projects that helped gitguild become reality.