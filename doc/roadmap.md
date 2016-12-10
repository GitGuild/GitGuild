# Flat CII file standards 
v0.0.2.1

Apply the CII standards to a flat repository, i.e. no submodules. This is the closest file structure we can adopt relative to existing, high quality FLOSS projects.

### issues

 + [x] configure_local
 + [x] init_flat
 + [x] register_flat
 + [x] status_flat

# Flat basic commit
v0.0.2.2

Commit gpg signed, status checked, changlog entered commit.

### issues

 + [x] file_templates
 + [ ] basic_commit

# Flat XP-only ledger
v0.0.2.3

Add ledger files back in, defining an XP asset for Experience Points. Create a contribute transaction template and command to credit contributors in XP.

### issues

 + [ ] contribute_XP_only
 + [ ] commit_contribution

# Flat XP-only ledger with voting
v0.0.2.4

Vote on contribution (and other?) changes, over multiple GPG-signed commits. Commits should be voted on in the 'voting' branch, and after passing, merged into 'consensus'.

### issues

 + [ ] issue_vote
