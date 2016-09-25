from ConfigParser import ConfigParser
from os import mkdir, remove, chdir, system, makedirs
import subprocess
from unittest import TestCase
from os.path import exists, join, isfile, abspath
from shutil import rmtree, copyfile, move

import ledger
import time
from git import Repo

from gitguild import gitname
from gitguild.gg import parser, cli
from gitguild.types import Guild

# NAME = 'isysd'
VOTE_RULES = {'FORK': 100,
              'CHARTER': 90,
              'SIDECHAIN': 85,
              'AGREEMENT': 75,
              'MEMBER': 51}
GGREPO = 'https://github.com/GitGuild/gitguild-cli.git'
GGDATAREPO = 'https://github.com/GitGuild/gitguild.git'
EMPTYREPO = 'https://github.com/GitGuild/empty_repo.git'
TESTDIR = './ggtest'
ABSDIR = abspath(TESTDIR)
if not exists(ABSDIR):
    makedirs(ABSDIR)
chdir(ABSDIR)


class TestFiles(TestCase):
    def setUp(self):
        system('rm -fR %s' % join(ABSDIR, "*"))

    def test_init(self):
        guild = Guild.create_stub_guild(path="./", vote_rules=VOTE_RULES)
        assert guild.basic_files_exist()
        for key in VOTE_RULES.keys():
            assert guild.vote_rules[key] == VOTE_RULES[key]
        assert not exists(join(ABSDIR, 'members', gitname))
        guild.register()
        guild.approve_member(gitname)

    # def test_create_stub_guild(self):
    #     guild = Guild.create_stub_guild(path="./", vote_rules=VOTE_RULES)
    #     with open(join(ABSDIR, 'charter.ledger'), 'w') as charter:
    #         for line in charter.readlines():
