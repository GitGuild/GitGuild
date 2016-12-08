import subprocess
from os import makedirs, system, chdir, fsync
from os.path import exists, join, isfile, abspath

import datetime
from git import Repo, Submodule
from git.repo.base import InvalidGitRepositoryError
from gitguild import GuildError


class Guild(object):
    _members = None
    _repo = None
    path = None
    _user_name = None
    _user_email = None
    _user_signingkey = None

    def __init__(self, path=None):
        self.path = abspath("./") if path is None else path
        self.repo  # initialize to ensure git repo exists
        self._members = {}

    @property
    def user_name(self):
        if self._user_name is None:
            try:
                self._user_name = subprocess.check_output(['git', 'config', 'user.name']).strip()
            except subprocess.CalledProcessError:
                self._user_name = None
                raise GuildError("Please configure a git user name.")
        return self._user_name

    @property
    def user_email(self):
        if self._user_email is None:
            try:
                self._user_email = subprocess.check_output(['git', 'config', 'user.email']).strip()
            except subprocess.CalledProcessError:
                raise GuildError("Please configure a git user email.")
        return self._user_email

    @property
    def user_signingkey(self):
        if self._user_signingkey is None:
            try:
                self._user_signingkey = subprocess.check_output(['git', 'config', 'user.signingkey']).strip()
            except subprocess.CalledProcessError:
                raise GuildError("Please configure a git user signingkey.")
        return self._user_signingkey

    @property
    def repo(self):
        if self._repo is None:
            self._repo = Repo(self.path)
        return self._repo

    @property
    def members(self):
        if self._members is None or len(self._members) == 0:
            authorpath = join(self.path, 'AUTHORS')
            with open(authorpath, 'r') as authorsf:
                for line in authorsf.readlines():
                    line = line.strip()
                    if len(line) == 0 or line.startswith("#"):
                        continue
                    else:
                        memarray = line.split(" ")
                        self._members[memarray[0]] = {'email': memarray[1], 'signingkey': str(memarray[2:])}
                authorsf.close()
        return self._members

    @classmethod
    def create_stub_guild(cls, path=None):
        if path is None:
            path = abspath("./")
        chdir(path)
        docdir = join(path, 'doc')
        authorpath = join(path, 'AUTHORS')
        if isfile(authorpath):
            raise GuildError('Cannot overwrite guild; file exists: %s' % authorpath)
            return
        contributingpath = join(path, 'CONTRIBUTING.md')
        if isfile(contributingpath):
            raise GuildError('Cannot overwrite guild; file exists: %s' % contributingpath)
            return
        changelogpath = join(path, 'CHANGELOG.md')
        if isfile(changelogpath):
            raise GuildError('Cannot overwrite guild; file exists: %s' % changelogpath)
            return
        if exists(docdir):
            raise GuildError('Cannot overwrite guild; dir exists: %s' % docdir)
        else:
            makedirs(docdir)
        issuesdir = join(docdir, 'issues')
        makedirs(issuesdir)
        makedirs(join(issuesdir, 'open'))
        makedirs(join(issuesdir, 'closed'))
        system("touch %s %s %s" % (authorpath, contributingpath, changelogpath))
        with open(contributingpath, 'w') as contributingfile:
            contributingfile.write("# GitGuild Contributing Stub\n")
            contributingfile.write("Write your own Contributing here\n")
            contributingfile.close()
        with open(changelogpath, 'w') as changelogf:
            changelogf.write("""
# Change Log

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

This Change Log format is suggested by
<https://github.com/olivierlacan/keep-a-changelog/blob/master/CHANGELOG.md>
""")
            changelogf.close()
        try:
            return cls(path=path)
        except InvalidGitRepositoryError:
            # Git repo has not been initialized. Do this now, since all guilds must live inside git repos.
            system("git init")
            return cls(path=path)

    def basic_files_exist(self):
        """
        Check for basic required file structure.
        """
        try:
            assert self.repo is not None
        except (InvalidGitRepositoryError, AssertionError):
            return False
        return (exists(self.path) and
                exists(self.path) and
                isfile(join(self.path, 'AUTHORS')) and
                isfile(join(self.path, 'CHANGELOG.md')) and
                isfile(join(self.path, 'CONTRIBUTING.md')))

    def register(self):
        if not self.basic_files_exist():
            raise IOError('No valid guild data found.')
            return

        if self.user_name in self.members:
            raise GuildError("User name %s already registered" % self.user_name)
        mempath = join(self.path, 'AUTHORS')
        with open(mempath, 'r+b') as memf:
            wfile = memf.read()
            if " %s " % self.user_email in wfile:  # TODO pretty inefficient query method
                memf.close()
                raise GuildError("User email %s already registered" % self.user_email)
            elif " %s\n" % self.user_signingkey in wfile:  # TODO pretty inefficient query method
                memf.close()
                raise GuildError("User signingkey %s already registered" % self.user_signingkey)
            else:
                memf.write("%s %s %s\n" % (self.user_name, self.user_email, self.user_signingkey))
                self._members[self.user_name] = {'email': self.user_email, 'signingkey': self.user_signingkey}
            memf.close()

    def member_status(self, name=None):
        name = name if name is not None else self.user_name
        ismember = True if name in self.members else False
        isuser = True if name == self.user_name else False

        if ismember and isuser:
            return "%s is one of the %s members" % (name, len(self.members))
        else:
            current = "current " if isuser else ""
            memnot = " not" if not ismember else ""
            raise GuildError("%s%s is%s one of the %s members" % (current, name, memnot, len(self.members)))

    def guild_status(self):
        if not self.basic_files_exist():
            raise GuildError("Not currently in a guild. Run 'init' command to create one.")
        else:
            return "Guild in good standing."
