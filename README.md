# gitguild

Guild-like governance for a git repository, using PGP identities.

IRC: #gitguild on freenode (see https://freenode.net/kb/answer/chat)

## Configure your user

Before using `gg`, you will be required to do some local configuration. This lets `gg` know about your pgp keys and configuration choices.

If you do not run `gg configure`, then the first command you attempt will run it for you.

__Example__
```
gg configure --name isysd --roles "maintainer contributor" --keyid B5D3D208 --pass-manage prompt --gnupg-home ~/.gnupg
```

## Charter a Guild

To charter a guild in the local directory (should be the top level of a git repo), run `gg charter`. A template must be provided, which contains a charter and role contracts.

```
$gg charter
Chartering new guild using template: software
Passphrase for keyid B5D3D208: 
```

## Register User

To register your user with the current working guild, use the `gg register` command. This will add your user to the guild membership roles as well as signing the charter and contract for you.

```
gg register
```

## Ledger Entries

__This section is still planned...__

### Record a Payment

__This section is still planned...__

```
gg add payment --amount 1 --currency "BTC" --txid "..." --user "Bob" --role "contributor" --reference "PR #27"
```

### Create a Bounty

__This section is still planned...__

gg add bounty --amount 1 --currency "BTC" --reference "issue #30"

## File Structure

For a repository to be conforming Git Guild, it must have the following file structure:

| Location | Description |
|----------|-------------|
| .gg/     | Git Guild data directory |
| .gg/charter.md | Charter for this repository |
| .gg/members.csv  | Registry of members, public keys, and roles |
| .gg/ledger.csv(.gpg) | A (encrypted?) ledger of accounts for this repository. Record of all credits, debits, and promises. |
| .gg/contracts/ | Directory for contract templates. Signed contracts belong in the signing user's signature directory. |
| .gg/contracts/$role.md  | Contract governing the responsibilities and benefits pertaining to the role named $role i.e. manager |
| .gg/users/ | Directory for all user specific documents. |
| .gg/users/$username/ | Directory storing all documents by the user with name $username |
| .gg/users/$username/$document.asc | The user's signature for a document i.e. charter.md |

So say we have a relatively simple repository like a website with a manager, two contributors and an arbitrator. Our members.csv might have content that looks like this:

| Name | Roles | Keyfp | Status |
|------|------|------------|--------|
|Alice | Manager | 2E945FC151AED70B230AD4DBD811F669651AA3E9 | active |
|Bob | Contributor | A5AE3894C77DBA19681C3C0B51DB916CBFF82D82 | active |
|Clair | Contributor | 0A3888126FA9ACA155002C12F8644E58C2F901A8 | active |
|Dean | Arbitrator | 606465EAE5A7ADDC237C93B9E09688F1B53995C8 | active |

The charter might say something very simple like "The Manager had complete control over membership, the treasury, as well as veto power on Pull Requests (PRs). In case of a dispute, the Arbitrator will judge, and the loser will pay Arbitrator 10% of the recovered amount."

Then each member, Alice, Bob, Clair, and Dean would sign `charter.md` and add the resulting file `charter.md.gpg` to their respective signature directories. Each must also sign the contract that corresponds to their role. For instance, Dean signs `arbitrator.md` and Alice signs `manager.md`. Finally, Alice must sign `roles.md`, as well as maintaining and signing `ledger.csv`.

If all of these files are up to date, the repository is considered in good standing.
