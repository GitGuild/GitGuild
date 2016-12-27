# Consensus

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

## Summary

If this seems too easy, you're not alone. For software developers, git feels like water to a fish. It is challenging to discover something new about the environment you survive in.

The contributors to Proof of Labor are amazed at how broad the applications seem to be. The natural contracting language and strong reputation system of PoL are unique in a blockchain. Due to this broad scope, we have erred on the side of abstraction over specification. While Proof of Labor could be even more loose, and many alternate implementations are possible, we believe this is a flexible, minimal working ruleset.

Proof of Labor is complimentary with PoW systems in many ways, and could even be applied after the fact as a governance layer to blockchains like Bitcoin. It could be used as an oracle by other blockchains, or lend them sidechain functionality. It is not likely to be as fast or as directly scalable, but perhaps with advanced sidechain usage, even massive parallel processing could be possible. Most likely, however, an optimal hybrid will emerge after much experimentation.
