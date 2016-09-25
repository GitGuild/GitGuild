from os import makedirs, system
from os.path import exists, join, isfile, abspath

import datetime

import ledger
import sys
from git import Repo, Submodule
from ledger import Amount

from ledger import Balance

from gitguild import gitname, gitsigkey


class Guild(object):
    Experience = Amount("0.00000000 XP")
    OffsetVotes = Amount("0.00000000 XP")
    Liabilities = Amount("0 XGG")
    Assets = Balance()
    _members = {}
    _votes = {}
    _vote_rules = {}
    _repo = None
    chain = None
    path = "./"
    ledger = "./chain.ledger"

    def __init__(self, path=None, vote_rules=None):
        self.path = "./" if path is None else path
        if vote_rules is not None:
            self._vote_rules = vote_rules
        else:
            self.load_vote_rules()
        self.load_chain()

    def load_vote_rules(self):
        start = False
        with open(abspath(join(self.path, "charter.ledger")), 'r') as charter:
            for line in charter.readlines():
                # print line
                if start:
                    if line.startswith("; END Vote Rules"):
                        # print "done"
                        break
                    else:
                        l2 = line.strip().split(" ")
                        l3 = l2[1].split("=")
                        self._vote_rules[l3[0].replace("_VOTES", "")] = Amount(l3[1])
                elif line.startswith("; BEGIN Vote Rules"):
                    start = True
                    # print "starting"

    def load_chain(self):
        self.chain = ledger.read_journal(abspath(join(self.path, "chain.ledger")))
        # for post in self.chain.query("/^m:*/"):
        for post in self.chain.query(""):  # get all postings
            # print post.account
            # print post.amount
            account_list = str(post.account).split(":")
            if account_list[0] == 'Experience':
                # print "guild member earned %s" % post.amount
                self.Experience += post.amount
            elif account_list[0] == 'OffsetVotes':
                # print "guild votes offset %s" % post.amount
                self.OffsetVotes += post.amount
            elif account_list[0] == 'Liability':
                # print "guild issued tokens %s" % post.amount
                self.Liabilities += post.amount
            elif account_list[0] == 'Assets':
                # print "guild has assets %s" % post.amount
                self.Assets += post.amount
            elif account_list[0] == 'm':
                if account_list[1] not in self._members:
                    # print "found member: %s" % account_list[1]
                    # account = self.chain.find_account_re("m:%s" % account_list[1])
                    self._members[account_list[1]] = Member(account_list[1], guild=self)
                if len(account_list) == 3:
                    # print "found posting for %s sub-account %s" % (account_list[1], account_list[2])
                    subaccount = getattr(self._members[account_list[1]], account_list[2])
                    setattr(self._members[account_list[1]], account_list[2], subaccount + post.amount)
                elif len(account_list) == 5:
                    assert account_list[2] == 'v'
                    # print "found %s vote record %s, %s" % (account_list[1], account_list[3], account_list[4])
                    vote_account = ":".join(account_list[2:])
                    if vote_account not in self._votes:
                        self._votes[vote_account] = Vote(self, account_list[1], account_list[2])
                    self._votes[vote_account].add_vote(post.amount, member=account_list[4])
                else:
                    raise IOError("invalid member account: %s" % post.account)
            elif account_list[0] == 'v':
                if len(account_list) == 3:
                    vote_account = str(post.account)
                    # print "found offset vote: %s" % vote_account
                    if vote_account not in self._votes:
                        self._votes[vote_account] = Vote(self, account_list[1], account_list[2])
                    self._votes[vote_account].add_vote(post.amount)
                else:
                    raise IOError("Unknown vote format: %s" % vote_account)
            else:
                raise IOError("Unknown posting account %s" % post.account)
        # self.chain.

    def validate_votes(self):
        for vote in self._votes:
            self._votes[vote].validate()

    def validate_members(self):
        for member in self._members:
            self._members[member].validate()

    @property
    def repo(self):
        if self._repo is None:
            self._repo = Repo(self.root)
        return self._repo

    @property
    def members(self):
        if len(self._members) == 0:
            self.load_chain()
        return self._members

    @property
    def vote_rules(self):
        if len(self._vote_rules) == 0:
            self.load_chain()
        return self._vote_rules

    @classmethod
    def create_from_gg_repo(cls, gg_repo, path='./', branch='master'):
        guild = Guild(path)
        Submodule.add(guild.repo, 'gg', guild.gg_path, gg_repo, branch=branch)

    @classmethod
    def create_stub_guild(cls, path=None, vote_rules={}):
        if path is None:
            path = "./"
        memdir = join(path, 'members')
        if not exists(memdir):
            makedirs(memdir)
            system("echo '' > %s" % join(memdir, 'members.ledger'))
        with open(join(path, 'charter.md'), 'w') as charterfile:
            charterfile.write("# GitGuild Charter Stub\n")
            charterfile.write("Write your own charter here")
            charterfile.close()
        with open(join(path, 'charter.ledger'), 'w') as ledgerfile:
            ledgerfile.write("""; BEGIN Vote Rules
define FORK_VOTES={0:.8f}
define CHARTER_VOTES={1:.8f}
define SIDECHAIN_VOTES={2:.8f}
define AGREEMENT_VOTES={3:.8f}
define MEMBER_VOTES={4:.8f}
; END Vote Rules
""".format(vote_rules['FORK'] / 100.0,
           vote_rules['CHARTER'] / 100.0,
           vote_rules['SIDECHAIN'] / 100.0,
           vote_rules['AGREEMENT'] / 100.0,
           vote_rules['MEMBER'] / 100.0))
            ledgerfile.write("""
; BEGIN Assets
account Assets
    note The Guild Treasury
    alias Treasury

account Liabilities
    note The Guild issues XGG from this account
    alias Printing Press
    ; assert commodity == "XGG"

account Experience
    note The Guild's Experience issuing account
    alias Ignorance
    assert commodity == "XP"

account OffsetVotes
    note Offset XP created for enforcing the vote rules
    ; assert commodity == "XGG"

commodity XP
   note Experience Points are non-transferable, reusable voting tokens
   format 1,000.00000000 XP
   nomarket
; END Assets
""")
            ledgerfile.close()
        with open(join(path, 'chain.ledger'), 'w') as ledgerfile:
            ledgerfile.write("""!include charter.ledger
!include ./members/members.ledger
; BEGIN Chart of Accounts
; END Chart of Accounts
!include block.ledger
""")
            ledgerfile.close()
        with open(join(path, 'block.ledger'), 'w') as ledgerfile:
            ledgerfile.write("""
%s * Founding
    Experience                     -1 XP
    m:%s:Experience             1 XP
""" % (datetime.datetime.utcnow().strftime('%Y/%m/%d %H:%M:%S'), gitname))
            ledgerfile.close()
        return cls(path=path, vote_rules=vote_rules)

    def basic_files_exist(self):
        """
        Check for basic required file structure.
        """
        return (exists(self.path) and
                exists(join(self.path, 'members')) and
                isfile(join(self.path, 'members', 'members.ledger')) and
                isfile(join(self.path, 'charter.md')) and
                isfile(join(self.path, 'charter.ledger')) and
                isfile(join(self.path, 'chain.ledger')) and
                isfile(join(self.path, 'block.ledger')))

    def register(self):
        if not self.basic_files_exist():
            raise IOError('No valid guild data found.')
            return

        memdir = join(self.path, 'members', gitname)
        if exists(memdir):
            raise IOError('Looks like you are already registered at %s' % memdir)
            return
        else:
            makedirs(memdir)

        system('echo "# {0} Profile" > {1}'.format(gitname, join(memdir, "%s.md" % gitname)))
        system('gpg -a --export {0} > {1}'.format(gitsigkey, join(memdir, "%s.asc" % gitsigkey)))
        with open(join(memdir, "%s.ledger" % gitname), 'w') as memledger:
            memledger.write("""account m:{0}
    note {1}
    assert commodity =~ /^XP|XGG$/

account m:{0}:Experience
    assert commodity == "XP"

account v:Member:{0}
    assert commodity == "XP"

account m:{0}:v:Member:{0}
    assert commodity == "XP"

= expr ( account == 'Experience' )
    v:Member:{0}                (MEMBER_VOTES)
    OffsetVotes                   (-MEMBER_VOTES)
""".format(gitname, gitsigkey))
        with open(join(self.path, 'members', 'members.ledger'), 'w') as memledger:
            memledger.write("!include ./{0}/{0}.ledger".format(gitname))

    def approve_member(self, username):
        """Vote for a specific member."""

        memdir = join(self.path, 'members', username)
        if not exists(memdir):
            raise IOError('That member is not registered')
            return

        with open(join(memdir, "%s.ledger" % gitname), 'a') as memledger:
            memledger.write("""

= expr ( account == 'm:{1}:Experience' )
    v:Member:{0}                  1.0
    m:{0}:v:Member:{1}            -1.0
""".format(username, gitname))


class Member(object):
    name = None
    status = 'pending'
    Experience = Amount("0.00000000 XP")
    Assets = Balance()
    Liabilities = Balance()

    def __init__(self, name, guild):
        self.name = name
        self.guild = guild

    # def validate(self):


class Vote(object):
    guild = None
    topic = None
    subject = None
    member = {}
    count = Amount("0.00000000 XP")

    def __init__(self, guild, topic, subject):
        self.guild = guild
        self.topic = topic
        self.subject = subject

    def add_vote(self, amount, member=None):
        # print "adding vote %s for member %s" % (amount, member)
        if member is not None:
            if member in self.member:
                self.member[member] += amount
            else:
                self.member[member] = amount
        else:
            self.count += amount

    def validate(self):
        calc_count = self.guild.Experience * self.guild.vote_rules["%s_VOTES" % self.topic.upper()]
        for member in self.member:
            # print "found %s %s:%s votes for member %s" % (self.member[member], self.topic, self.subject, member)
            assert member in self.guild.members
            spent = abs(self.member[member])
            assert spent <= self.guild.members[member].Experience
            calc_count += spent
        assert calc_count == self.count
