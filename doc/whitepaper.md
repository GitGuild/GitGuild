# Git Guild Blockchain

*A git guild is a git-native contract and payment network.*

__Document version 0.2.0__

## Abstract

Git is a flexible version control system in use by tens of millions of collaborators worldwide. Git [stores data](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects) in sha1 hash trees, and [supports](https://git-scm.com/book/en/v2/Git-Tools-Signing-Your-Work) gpg signing of commits (since v1.7.9). With strict usage guidelines, these cryptographic utilities create a blockchain made up of gpg-signed, sha1-hashed commits.

## Proof of Labor

A chain of signed commits is hearafter referred to as Proof of Labor. Proof of Labor is a flexible, meritocratic mining system.

Each block of data is made up of a pgp-signed git commit. This commit consistitutes some Labor performed by one or more members of the guild. The other members of the guild then vote on accepting the PR or not by merging the commit or creating a fork.

Once a commit has been merged into the master branch, it may not be reverted or overwritten without being detected by other members of the guild. Git guild are immutable unless a fork aka rebase is explicitely voted for. This is similar to other blockchains, where immutability is subject to maintaining consensus.

#### Crypto

While this system has not yet been reviewed by cryptographers, it should not be controversial. Proof of Labor uses standard, well established tools in a downright orthodox way.  

GNU Privacy Guard aka GPG is a popular encryption program first released in 1999. GPG is open source software package compliant with [RFC 4880](https://tools.ietf.org/html/rfc4880), which is the IETF standards track specification of OpenPGP. The latest version (2.0.30) supports RSA, ElGamal and DSA signing, as well as a number of ciphers, hashes, and compression algorithms. It is commonly used for encrypting and/or signing emails, and is growing in use in the git community.

Git was developed as a file system, by Linus Torvalds, in 2005. The SHA1 hash tree that git uses was introduced in that first version. Since git has become one of the most popular software projects of all time, this hash tree has seen a lot of real world use, as well as development. Key to the hash tree is that all files are hashed into a commit, along with the parent commit(s). Git's hash tree is a directed acyclic graph. This means it is a one directional, immutable tree with branches and branch resolution. Loops, rewriting history, and a number of other logical inconsistencies are prevented.

Since git v1.7.9, released in 2012, git has supported GPG signing commits. This release was the final technical pre-requisite for Proof of Labor.

## Rules & Requirements

The following rules of git and other software usage are necessary for the Proof of Labor model to function.

| Rule | Description |
|-------|----------------|
| Must sign | Every commit must be signed by a signature of a member to be considered for merge. |
| Member branches | A member's branch is their vote on the state and contents of the chain. Only the member is allowed to sign their own branch. |
| Must merge votes | Any new master block must include every passing vote. Basically, master branch is consensus of valid votes. |
| Auto-merge conflict resolution | Votes that are non-conflicting but behind the master branch must be merged. |
| Higher | Every commit must have a higher `<guild_name>:Height` than it's parent.  |
| Highest | Consensus is the highest valid branch of a guild. This should be mirrored to master and the guild's own branch as commits are made to member branches. |
| Max Depth | Each member can only vote up to their total `<user_name>:Height` on each parent hash. |

The first four rules are all git best practices. These rules, and the automation of execution of checks on them, ensure a complete chain of responsibility for each change. Incomplete usage of gpg signing is not nearly good enough, as Mike Gerwitz points out in [A Git Horror Story: Repository Integrity With Signed Commits](https://mikegerwitz.com/papers/git-horror-story.html).

"[H]ow can you be sure that their commits are actually their own? Furthermore, how can you be sure that any commits they approve (or sign off on using git commit -s) were actually approved by them?

That is, of course, assuming that they have no ill intent. For example, what of the pissed off employee looking to get the arrogant, obnoxious co-worker fired by committing under the coworker’s name/email? What if you were the manager or project lead? Whose word would you take? How would you even know whom to suspect?"

The answer to these questions is strict standards and enforcement, i.e. rules 1-4.

The last three rules are all for ledger use, and ensure consensus is calculated and enforced. Git actions are recorded by spending XP in the ledger in `Height` and `Depth` accounts. The amount of XP in the `Height` of any commit determines it's acceptance or rejection by the organization, and therefore it's mergability into master.

#### Branches

Proof of Labor uses git branches for its data structure, and so needs strict control of these. The following keywords are reserved branch names.

| Branch             | Maintainer       | Description           |
|--------------------|--------------------|------------------------|
| master             | Last to commit  | The master branch is a protected communal branch. It reflects the latest valid state of the sum of all member branches. |
| username             | username  | Each member must maintain their own branch, and use this branch for submitting votes (commits) or voting on the commits of others (merging). |

Currently a trusted git server is used as the source of truth. The master branch must always be kept in a signed and complete state. Git's hash tree is also independently maintained by each member, serving as a complete, independent record of events. There are many ways this basic hosting setup can be enhanced, such as inserting the master commit hashes into a proof of work blockchain.

#### Members

Members apply to a guild by creating branch named after themselves, adding themselves to `AUTHORS`, adding their accounts and checks to the ledger files, adding a file with their ssh public key to the `keydir` directory, and committing the gpg-signed result. The existing members then vote, and, if the XP approval threshold is reached, the new user branch is merged, accepting the member into the guild.

Because usernames are used throughout the guild data structures, a number of names are forbidden. As of now, usernames may only contain letters, numbers, `-`, and `_`. Note that usernames are not case-sensitive. The following keyword(s) are also reserved as forbidden usernames.

| Name               | Reason Forbidden       |
|--------------------|------------------------|
| master             | Keyword for the consensus branch. |

## Summary

If this seems too easy, you're not alone. For software developers, git feels like water to a fish. It is challenging to discover something new about the environment you survive in.

The contributors to Proof of Labor are amazed at how broad the applications seem to be. The natural contracting language and strong reputation system of PoL are unique in a blockchain. Due to this broad scope, we have erred on the side of abstraction over specification. While Proof of Labor could be even more loose, and many alternate implementations are possible, we believe this is a flexible, minimal working ruleset.

Proof of Labor is complimentary with PoW systems in many ways, and could even be applied after the fact as a governance layer to blockchains like Bitcoin. It could be used as an oracle by other blockchains, or lend them sidechain functionality. It is not likely to be as fast or as directly scalable, but perhaps with advanced sidechain usage, even massive parallel processing could be possible. Most likely, however, an optimal hybrid will emerge after much experimentation.

#### Living Document

Don't take our word for it. This paper is governed by [a guild](https://github.com/GitGuild/GitGuild/tree/master). Try the bundled alpha client to demo and register with the founding guild.
