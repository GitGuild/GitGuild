# gitguild

Guild governance for a git repository, using PGP identities.

IRC: #gitguild on freenode (see https://freenode.net/kb/answer/chat)

 + Issue digital value tokens
 + Create, sign, and enforce contracts
 + Participate in projects in a democratic, decentralized manner

## Try it out

Since this version of `gitguild` is a bourne shell script, it should be runnable as a standalone program on linux based systems. Macs and windows machines will definitely work with some work on the prerequisites. Just don't run setup with extra options, if you're only trying it out, i.e. no `--gitolite`.

## Install

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

## CLI

This program is a command line suppliment to git. As the command line is the primary way users are expected to interact with gitguild, the help menus are comprehensive.

```
	gitguild           	A helpful blockchain in a script.

	Usage:
		gitguild user	Manage your gitguild user.
		gitguild tx	    build and check transactions.
		gitguild push	git push with extra checks and remotes.
		gitguild fork	fork	<remote> Fork a guild with one or more remotes.
		gitguild setup	    Install pre-requisites and configure gitguild.
		gitguild template	Create and list tx templates.
		gitguild help		Show the general help.
		gitguild version	    Show the program version.

	Options:
		gitguild <cmd> -h	Show command help details.

```

## Additional Resources

Guilds keep all documentatation, issues, and other project-relevant information inside the repository. There are a number of detailed documents in the top level of this directory that are a good place to start.

### General

 + docs/faq.md

### Technical

 + docs/roadmap.md
 + docs/file-structure.md
 + docs/templates.md
 + docs/ledger.md


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