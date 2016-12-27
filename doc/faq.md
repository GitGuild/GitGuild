# Frequently Asked Questions (FAQ)

### The GitGuild Organization

##### Mission Statement

The GitGuild is a development cooperative building tools, methodologies, and operational models that empower FLOSS projects to achieve financial and technical independence without compromising on principles.

##### What is the GitGuild?

The GitGuild is a community of developers, designers and other contributors, dedicated to open, transparent, and mutually-profitable organizational principles. This is managed through universally accessible and naturally democratic tools of [Git](http://git-scm.com/), [PGP](https://gnupg.org/), and [ledger-cli](http://ledger-cli.org/).

##### How does a Guild operate?

"The" GitGuild is different from "a" Guild using the GitGuild methodologies.

A Guild operates by establishing a constitution (aka CONTRIBUTING.md), contracts (templates), and recruiting members. Documents are stored publicly, accessible by all, and members sign every action with pgp.

Each guild must maintain a ledger allocating XP to users, which they then spend voting on commits. The gitguild software uses this XP commit voting structure to calculate the consensus for the organization.

##### How does the GitGuild operate?

"The" GitGuild is different from "a" Guild using the GitGuild methodologies.

The GitGuild is an experimental Guild that was established to empower open source software development teams. We function like any other guild, but using experimental tools and models before they're recommended for general use.

In addition to developing the core technology, the GitGuild maintains a registry of active guilds, and may provide some hosting/mirroring services. This is essential for cross referencing guilds, and keeping them in sync. Over time, other organization guilds will bridge these gaps between individuals, but at the start, the GitGuild will be the only option available.

##### Does the GitGuild share everything it produces?

Yes. Our software is all released under a MIT license. Legal, operational, and other methodological documents are released under a Creative Commons license.

### What projects does the GitGuild maintain?

##### Core

 + [gitguild command software](https://github.com/gitguild/gitguild)
 + [gitguild.com website](https://github.com/gitguild/gitguild_website) (10% complete)  

##### Other Projects

 + [bitjws](https://github.com/deginner/bitjws) - Bitcoin message signing and JWS combined to an autentication standard similar to bitid.
 + De application framework - This really has no name, but we have a whole application framework built up around bitjws, swagger, and sqlalchemy. Multiple github repositories for servers, clients, etc.
 + [desw](https://github.com/deginner/desw) - a multi-currency hot wallet service available via API.
 + [De Broker](https://github.com/deginner/de-broker) - a fixed-price cryptocurrency brokerage ala Shapeshift
 + [De Exchange Node](https://github.com/deginner/exchange-node) - a bid/ask exchange engine and orderbook.
 + De Cosigner - An automated cosigning service to compliment bitcore or other multisignature wallet clients.
 + [Trade Manager](https://github.com/deginner/trade-manager) - An exchange client manager for manual or automated trading on popular cryptocurrency exchanges.

### GitGuild and Me

##### Can I personally become a GitGuild member?

Yes! Anyone can join, and use our software, XGG coin, as well as network services. The GitGuild exists to develop software, however, and if you wish to earn XP in the GitGuild, you must do some constructive work and earn XGG Income.  

GitGuild members are also subject to XP vote approval, and must maintain a minimum of 50% approval to access organization services.

##### Does the GitGuild have any partners? Support external teams?

Yes, we support and are supported by the following projects and more.

 + [Tigo CTM](http://tigoctm.com)
 + [Dash](https://dash.org)
 + [200 Social](http://200social.com)
 + [Bitt](https://bitt.com)
 + [Coinapult](https://coinapult.com)
 + [Crypto Capital](https://cryptocapital.co)
 + [VeMine](https://vemine.org)

##### Can the GitGuild help my team build XYZ? Monetize our open source project? Reach internet users?

Yes! As an internet-based community of builders, we have all of the expertise and many of the components ready to assemble.

Our specialties are:

 + Digital currency issuance, management, liquidity, and launch
 + Trustless applications and services
 + Market services, such as exchange, brokerage, trading

##### Does the GitGuild provide financing for startup projects?

Yes, and no. If your project is a technical fit, and has commercial potential, then the GitGuild may offer to finance your project with GitGuild coin (XGG). This can be spent on development of your project with qualified, peer-reviewed GitGuild contributors. For many projects, this is sufficient to reach MVP, and market validation or failure.

Of course, the value paid to the contributors who build your MVP has to come from somewhere. Any XGG issued has to be in return for equal or greater value to the GitGuild. For instance, you may be asked to give up equity, pay digital tokens, or to make a revenue sharing agreement with the GitGuild.  

All such agreements require XP approval of 66%.


### GitGuild vs. Other Blockchains

##### Is GitGuild more or less private than Bitcoin?

That is a tough question to answer. GitGuild has very strong identities, and no throwaway addresses. These mean that parties to a transaction know a lot about each other, at minimum email and gpg key.  
  
On the other hand, the nature of the Bitcoin blockchain is inherently public. All addresses and transactions *must* be published in Bitcoin. This is not so for GitGuild, where private networks of ssh tunnels allow for completely private blockchains.

These private gitguild chains would have 100% encrypted traffic, using ssh keys, and could encrypt any messages to each other with their known email and gpg keys. Such an organization would be very private indeed.

##### Is GitGuild more or less decentralized than Bitcoin?

Definitely less, for now. GitGuild's P2P network is still under construction, and so [github](https://github.com) is most likely to be a central reference point for most guilds. Even after the P2P network launch, it can be expected that many projects will prefer their current git host over a change requiring some work.

##### Is GitGuild more or less scalable than Bitcoin?

Interesting question. The answer is not clear.

A single guild could probably not scale nearly as well as Bitcoin, because the data structures are significantly less efficient. The consensus algorithm is also not nearly as robust, designed to mirror human workflow, not provable computer work.
  
On the other hand, GitGuild is designed for parallelisation. Could a million guilds operate in parallel? Would that be more efficient than Bitcoin could be? How efficient can Bitcoin become with lightning, rootstock, and other parallelisation models? We don't know the answers to these questions yet.
