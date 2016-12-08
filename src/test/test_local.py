from ConfigParser import ConfigParser
from os import mkdir, remove, chdir, system, makedirs, fsync
import subprocess
from unittest import TestCase
from os.path import exists, join, isfile, abspath
from shutil import rmtree, copyfile, move
import psutil
import ledger
import time
from git import Repo

from gitguild.command import parser, cli
from gitguild.types import Guild, GuildError

# NAME = 'isysd'
GGREPO = 'https://github.com/GitGuild/gitguild-cli.git'
GGDATAREPO = 'https://github.com/GitGuild/gitguild.git'
EMPTYREPO = 'https://github.com/GitGuild/empty_repo.git'
TESTDIR = '/tmp/ggtest'
ABSDIR = abspath(TESTDIR)
if not exists(ABSDIR):
    makedirs(ABSDIR)
chdir(ABSDIR)


def get_or_invent_config(testcase):
    local_user_name = 'UniqUser'
    if testcase.global_user_name is not None:
        local_user_name = testcase.global_user_name
    elif testcase.local_user_name is not None:
        local_user_name = testcase.local_user_name
    local_user_email = 'test@gitguild.com'
    if testcase.global_user_email is not None:
        local_user_name = testcase.global_user_email
    elif testcase.local_user_email is not None:
        local_user_email = testcase.local_user_email
    local_user_signingkey = '51234'
    if testcase.global_user_signingkey is not None:
        local_user_signingkey = testcase.global_user_signingkey
    elif testcase.local_user_signingkey is not None:
        local_user_signingkey = testcase.local_user_signingkey
    system('git config --local --add user.name %s' % local_user_name)
    system('git config --local --add user.email %s' % local_user_email)
    system('git config --local --add user.signingkey %s' % local_user_signingkey)
    return local_user_name, local_user_email, local_user_signingkey


def clean_testdir():
    system('rm -fR %s' % join(ABSDIR, "*"))
    chdir(ABSDIR)


def cache_config(testcase):
    try:
        testcase.global_user_name = subprocess.check_output(['git', 'config', '--global', 'user.name']).strip()
    except subprocess.CalledProcessError:
        testcase.global_user_name = None
    try:
        testcase.global_user_email = subprocess.check_output(['git', 'config', '--global', 'user.email']).strip()
    except subprocess.CalledProcessError:
        testcase.global_user_email = None
    try:
        testcase.global_user_signingkey = subprocess.check_output(['git', 'config', '--global', 'user.signingkey']).strip()
    except subprocess.CalledProcessError:
        testcase.global_user_signingkey = None
    system('git config --global --unset-all user.name')
    system('git config --global --unset-all user.email')
    system('git config --global --unset-all user.signingkey')
    try:
        testcase.local_user_name = subprocess.check_output(['git', 'config', 'user.name']).strip()
    except subprocess.CalledProcessError:
        testcase.local_user_name = None
    try:
        testcase.local_user_email = subprocess.check_output(['git', 'config', 'user.email']).strip()
    except subprocess.CalledProcessError:
        testcase.local_user_email = None
    try:
        testcase.local_user_signingkey = subprocess.check_output(['git', 'config', 'user.signingkey']).strip()
    except subprocess.CalledProcessError:
        testcase.local_user_signingkey = None
    system('git config --local --unset-all user.name')
    system('git config --local --unset-all user.email')
    system('git config --local --unset-all user.signingkey')


def restore_cached_config(testcase):
    if testcase.global_user_email is not None and len(testcase.global_user_email) > 0:
        system('git config --global --add user.email %s' % testcase.global_user_email)
    if testcase.global_user_name is not None and len(testcase.global_user_name) > 0:
        system('git config --global --add user.name %s' % testcase.global_user_name)
    if testcase.global_user_signingkey is not None and len(testcase.global_user_signingkey) > 0:
        system('git config --global --add user.signingkey %s' % testcase.global_user_signingkey)
    system('git config --local --unset-all user.name user.email user.signingkey')
    if testcase.local_user_email is not None and len(testcase.local_user_email) > 0:
        system('git config --local --add user.email %s' % testcase.local_user_email)
    if testcase.local_user_name is not None and len(testcase.local_user_name) > 0:
        system('git config --local --add user.name %s' % testcase.local_user_name)
    if testcase.local_user_signingkey is not None and len(testcase.local_user_signingkey) > 0:
        system('git config --local --add user.signingkey %s' % testcase.local_user_signingkey)


class TestFiles(TestCase):
    def setUp(self):
        clean_testdir()

    def test_init(self):
        guild = Guild.create_stub_guild(path=ABSDIR)
        assert guild.basic_files_exist()

    def test_init_full(self):
        Guild.create_stub_guild(path=ABSDIR)
        try:
            guild = Guild.create_stub_guild(path=ABSDIR)
        except GuildError as e:
            assert e.message == 'Cannot overwrite guild; file exists: %s' % join(ABSDIR, 'AUTHORS')
            return
        assert guild == "should have thrown an exception"


class TestConfig(TestCase):
    def setUp(self):
        clean_testdir()
        cache_config(self)

    def tearDown(self):
        restore_cached_config(self)

    def test_config_fresh(self):
        guild = Guild.create_stub_guild(path=ABSDIR)
        try:
            assert guild.user_name is None
        except GuildError as ge:
            assert ge.message == "Please configure a git user name."
        try:
            assert guild.user_email is None
        except GuildError as ge:
            assert ge.message == "Please configure a git user email."
        try:
            assert guild.user_signingkey is None
        except GuildError as ge:
            assert ge.message == "Please configure a git user signingkey."
        local_user_name, local_user_email, local_user_signingkey = get_or_invent_config(self)
        assert guild.user_name == local_user_name
        assert guild.user_email == local_user_email
        assert guild.user_signingkey == local_user_signingkey


class TestRegister(TestCase):
    def setUp(self):
        clean_testdir()
        cache_config(self)

    def tearDown(self):
        restore_cached_config(self)

    def test_register(self):
        local_user_name, local_user_email, local_user_signingkey = get_or_invent_config(self)
        guild = Guild.create_stub_guild(path=ABSDIR)
        assert len(guild.members) == 0
        guild.register()
        assert len(guild.members) == 1
        assert local_user_name in guild.members
        assert len(guild.members[local_user_name]) == 2
        assert guild.members[local_user_name]['email'] == local_user_email
        assert guild.members[local_user_name]['signingkey'] == local_user_signingkey
        with open(join(ABSDIR, 'AUTHORS'), 'r') as f:
            assert "%s %s %s" % (local_user_name, local_user_email, local_user_signingkey) in f.read()
            f.close()

    def test_register_again(self):
        local_user_name, local_user_email, local_user_signingkey = get_or_invent_config(self)
        guild = Guild.create_stub_guild(path=ABSDIR)
        assert len(guild.members) == 0
        guild.register()
        assert len(guild.members) == 1
        assert local_user_name in guild.members
        assert len(guild.members[local_user_name]) == 2
        assert guild.members[local_user_name]['email'] == local_user_email
        assert guild.members[local_user_name]['signingkey'] == local_user_signingkey
        with open(join(ABSDIR, 'AUTHORS'), 'r') as f:
            assert "%s %s %s" % (local_user_name, local_user_email, local_user_signingkey) in f.read()
            f.close()

    def test_register_duplicate_name(self):
        local_user_name, local_user_email, local_user_signingkey = get_or_invent_config(self)
        guild = Guild.create_stub_guild(path=ABSDIR)
        assert len(guild.members) == 0
        guild.register()
        assert len(guild.members) == 1
        assert local_user_name in guild.members
        try:
            guild.register()
        except GuildError as ge:
            assert ge.message == "User name %s already registered" % local_user_name

    def test_register_duplicate_email(self):
        local_user_name, local_user_email, local_user_signingkey = get_or_invent_config(self)
        guild = Guild.create_stub_guild(path=ABSDIR)
        assert len(guild.members) == 0
        guild.register()
        assert len(guild.members) == 1
        assert local_user_name in guild.members
        assert len(guild.members[local_user_name]) == 2
        assert guild.members[local_user_name]['email'] == local_user_email
        assert guild.members[local_user_name]['signingkey'] == local_user_signingkey
        changed_user_name = "eve"
        system('git config --local --unset-all user.name')
        system('git config --local --add user.name %s' % changed_user_name)
        guild._user_name = changed_user_name
        try:
            guild.register()
        except GuildError as ge:
            assert ge.message == "User email %s already registered" % local_user_email

    def test_register_duplicate_signingkey(self):
        local_user_name, local_user_email, local_user_signingkey = get_or_invent_config(self)
        guild = Guild.create_stub_guild(path=ABSDIR)
        assert len(guild.members) == 0
        guild.register()
        assert len(guild.members) == 1
        assert local_user_name in guild.members
        assert len(guild.members[local_user_name]) == 2
        assert guild.members[local_user_name]['email'] == local_user_email
        assert guild.members[local_user_name]['signingkey'] == local_user_signingkey
        changed_user_name = "eve"
        system('git config --local --unset-all user.name')
        system('git config --local --add user.name %s' % changed_user_name)
        guild._user_name = changed_user_name
        changed_user_email = "eve@hax0r.com"
        system('git config --local --unset-all user.email')
        system('git config --local --add user.email %s' % changed_user_email)
        guild._user_email = changed_user_email
        try:
            guild.register()
        except GuildError as ge:
            assert ge.message == "User signingkey %s already registered" % local_user_signingkey


class TestStatus(TestCase):
    def setUp(self):
        clean_testdir()
        cache_config(self)

    def tearDown(self):
        restore_cached_config(self)

    def test_status_empty(self):
        guild = Guild.create_stub_guild(path=ABSDIR)
        clean_testdir()
        try:
            guild_status = guild.guild_status()
            assert "should not hit this line" is False
        except GuildError as ge:
            assert ge.message == "Not currently in a guild. Run 'init' command to create one."

    def test_status_good(self):
        local_user_name, local_user_email, local_user_signingkey = get_or_invent_config(self)
        guild = Guild.create_stub_guild(path=ABSDIR)
        try:
            guild.member_status(local_user_name)
            assert "should not hit this line" is False
        except GuildError as ge:
            assert ge.message == "current %s is not one of the 0 members" % local_user_name
        try:
            guild.member_status('username')
            assert "should not hit this line" is False
        except GuildError as ge:
            assert ge.message == "username is not one of the 0 members"
        guild.register()
        guild_status = guild.guild_status()
        assert guild_status == "Guild in good standing."
        member_status = guild.member_status()
        assert member_status == "%s is one of the 1 members" % local_user_name
