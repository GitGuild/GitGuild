# Alpha
v0

For use by GitGuild members and partners. Not intended for general user adoption.

## Experimental
v0.2

The GitGuild is a dynamic experiment in blockchain technology.
It is immutable, but far more flexible than other blockchains.
These early v0.0.x verions are experiments, meant to change over time.

### Data structures
v0.2.1

Experiments in data structures. These are the core contracts that make up a guild.

#### Flat CII file standards 
v0.2.1.1

Apply the CII standards to a flat repository, i.e. no submodules. This is the closest file structure we can adopt relative to existing, high quality FLOSS projects.

##### issues

 + [x] configure_local
 + [x] init_flat
 + [x] register_flat
 + [x] status_flat

#### Flat basic commit
v0.2.1.2

Commit gpg signed, status checked, changlog entered commit.

##### issues

 + [x] file_templates
 + [x] basic_commit

#### Flat XP-only ledger
v0.2.2

Add ledger files back in, defining an XP asset for Experience Points. Create a contribute transaction template and command to credit contributors in XP.

##### issues

 + [ ] contribute_XP_only

#### Local git server
v0.2.5

Each user is to run their own git server, using gitolite.
The gitolite admin repo will be merged with the guild identity repo, keeping the ledger and permissions in the same area.

 + [x] gitolite server setup and configuration
 + [x] gitolite admin repo merged with identity repo
 + [ ] Mirror to github

#### Flat XP-only ledger with voting
v0.2.6

Vote on contribution (and other?) changes, over multiple GPG-signed commits. Commits should be voted on in individual branches, and after passing, merged into the guild named branch.

##### issues

 + [ ] issue_vote

#### Pedantic and Secure Ledger
v0.2.7

Assure voting and other rules are enforced strictly at the ledger level.
Use check.ledger to run vote count and other guild-level assertions.

 + [ ] commit_contribution
 + [ ] check own commit
 + [ ] check other's commit

#### Document and UX test
v0.2.9

Clean up the code, documenting along the way. Prepare for others to review and contribute. Also use in the context of a git project, and test for helpfulness.

 + [ ] Account structure and relationship to voting
 + [ ] Height, Depth, and vote consensus
 + [ ] Network architecture, message flow
 + [x] Local software architecture, i.e. requirements, key rings, gitolite resources, git working dirs 

#### Alpha Test release
v0.3

This release will have all basic functionality, but may have bugs, even known bugs. It is intended for the GitGuild dev and QA team to familiarize themselves and give feedback before proceeding.

 + [ ] Package up and release to team
