# Ledger

Each guild should keep a ledger file using the [ledger-cli](http://ledger-cli.org) data format. This double entry accounting system is both human readable and mathematically accurate. Furthermore it is flexible enough to track or even create any currency, commodity, or digital token.  

### Account Structure

Account structure is quite complex in the GitGuild, creating a symmetry between this ledger and the git tree itself.

A number of complex and potentially long account names may be difficult to read, but they're quite organized. The basic structure is as follows.

`user_name:accounting_category:repository:branch:parent_commit_hash:metadata`

##### Voting and Consensus

If the account is a child of `Height` or `Depth`, then the last level is reserved for XP votes. Members spend XP from the guild's `Depth` account and assign it to member's `Height` for specific commits. This is done automatically when merging a commit, mathematically signalling the approval and weight of the merger's reputation.

##### Account Level 1

*user_name*

The top level of a guild ledger is the users themselves. Each account (except the guild account) belongs to exactly one user. Since no user can have the same name as the guild, this is a conflict free namespace with clear borders and responsibility.

For instance, the GitGuild communal accounts are `gitguild:*`, and in the gitguild ledger members have individual accounts, like isysd's `isysd:*`.

##### Account Level 2

*accounting_category*

The second level accounts are mostly traditional: `Income`, `Expenses`, `Assets`, `Liabilities`, `Equity`. These should be familiar to anyone with an accounting background, but ledger-cli also has an [excellent introduction](http://ledger-cli.org/3.0/doc/ledger3.html#Structuring-your-Accounts).

The second level also has two additional options related to voting: `Height`, `Depth`. Depth is where XP originates, and where each member spent XP is counted. Height is where XP are spent and issues votes are counted. So each XP originates in some `Depth` and then goes to a `Height`. These are key to determining consensus, and enforcing the guild's rules.

Each transaction requiring an XP vote must list itself in the signing user's Height. The more + XP that any account accumulates, the more standing it has in the guild. The guild's total height is how forward progress is measured, and no commit can have a lower total height than it's parent.

##### Account Level 3

*repository*

From the third level on, accounts mirror the git structure closely. This is a sort of address system, allowing a ledger consumer to identify the repository, branch, and commit associated with a balance. Level 3 is the repository level. Assuming the client already has a remote list for each repository, it is enough information to begin the search.

It is important to note that each user must have a personal guild, which is a repository. Every guild must be a repository, but not every repository is a guild. Still, with every possible name combination, this repository namespace has no room for non-user-name, non-guild-name repositories. Such repositories cannot safely be recorded in a guild ledger.

##### Account Level 4

*branch*

Inside each repository are branches. These are also named after users, and represent each user's perspective on the repository. Again, the namespace is restricted only to the names of users and guilds, forbidding alternatives.

##### Account Level 5

*parent*

Parent is the SHA1 hash of the parent commit to the one containing the transaction. This is the last bit of information in the git tree address: repository, branch, commit hash. Once these are specified, the transaction is unambiguously identified and can be treated individually for voting and other accounting operations.

##### Account Level 6

*metadata*

Metadata might be bitcoin or dash addresses, and/or transaction hashes. Really, this area is pretty open to any string important enough to be hashed into the ledger itself.
