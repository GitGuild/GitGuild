# Contributing

Feedback and contributions are very welcome!

## A GitGuild Project

This project uses [GitGuild](https://github.com/GitGuild/gitguild) software to govern itself and all contributions. Please [install](https://github.com/GitGuild/gitguild#install) the client to ensure you meet the strict configuration and usage requirements. These include, but are not limited to the following.

| Rule | Description |
|-------|----------------|
| Must sign | Every commit must be GPG signed by a member listed in the AUTHORS file. |
| Consensus branches | The `master` and `gitguild` branches are reserved for consensus. Only commits approved by XP vote can be merged. |
| Member branches | A member's branch is their vote on the state and contents of the chain. |
| Higher | Every commit must have a higher `<guild_name>:Height` than it's parent.  |
| Highest | Consensus is the highest valid branch of a guild. This should be mirrored to master and the guild's own branch as commits are made to member branches. |
| Max Depth | Each member can only vote up to their total `<user_name>:Height` on each parent hash. |

The first three rules are all git best practices. These rules, and the automation of execution of checks on them, ensure a complete chain of responsibility for each change. Incomplete usage of gpg signing is not nearly good enough, as Mike Gerwitz points out in [A Git Horror Story: Repository Integrity With Signed Commits](https://mikegerwitz.com/papers/git-horror-story.html).

"[H]ow can you be sure that their commits are actually their own? Furthermore, how can you be sure that any commits they approve (or sign off on using git commit -s) were actually approved by them?

That is, of course, assuming that they have no ill intent. For example, what of the pissed off employee looking to get the arrogant, obnoxious co-worker fired by committing under the coworker’s name/email? What if you were the manager or project lead? Whose word would you take? How would you even know whom to suspect?"

The answer to these questions is strict standards and enforcement, i.e. rules 1-3.

The last three rules are all for [ledger](https://ledger-cli.org) use, and ensure consensus is calculated and enforced. Git actions are recorded by spending XP in the ledger in `Height` and `Depth` accounts. The amount of XP in the `Height` of any commit determines it's acceptance or rejection by the organization, and therefore it's mergability into master.

## Payment

Contributors can request payment in GitGuild coin (XGG) as part of the contribution, and are allowed to redeem this XGG for BTC, DASH or other assets. If the commit is approved by the other members, the XGG will be counted as Income, also triggering a corresponding XP increase for the contributor.

Like every change made to a guild, this payment request process is templated in a patch file, and should be run using `gitguild tx build`. In this case the tx name is `paid_contribution`.

Though there are no set limits or rules on how much you can ask to be paid, remember that the pay is subject to review and approval by your peers. It is the very people reviewing your code that ultimately decide any pay you receive.

## Vulnerability reporting (security issues)

If you find a significant vulnerability, or evidence of one,
please send an email to the security contacts that you have such
information, and we'll tell you the next steps.
For now, the security contacts are:
isysd <ira@gitguild.com>, and
cindy-zimmerman <cindy@tigoctm.com>.  

Please use the PGP keys provided in the AUTHORS file to encrypt your message!

### Copyright

This file adapted from the Linux Foundation's Core Infrastructure Initiative's [CONTRIBUTING.md](https://github.com/linuxfoundation/cii-best-practices-badge/blob/master/CONTRIBUTING.md).

##### Open Source License (MIT)

All (new) contributed material must be released under the [MIT license](./LICENSE).
All new contributed material that is not executable, including all text when not executed, is also released under the [Creative Commons Attribution 3.0 International (CC BY 3.0) license](https://creativecommons.org/licenses/by/3.0/) or later.
