from ConfigParser import ConfigParser
from os import mkdir, remove
from unittest import TestCase
from os.path import exists, join, isfile, abspath
from shutil import rmtree, copyfile

from StringIO import StringIO

from git import Repo

from gitguild.gg import parser, cli, configure, load_config, basic_files_exist, status, charter

NAME = 'isysd'
ROLES = '"maintainer tester"'
KEYID = '0368383B7397C34B159A17E0C82DE5DFF1C475AF'
TMPDIR = '/tmp/ggtest'
GPGHOME = abspath('./test/gpg')
GGREPO = 'https://github.com/GitGuild/gitguild.git'
GGDATAREPO = 'https://github.com/GitGuild/gg_data.git'
EMPTYREPO = 'https://github.com/GitGuild/empty_repo.git'


class TestConfigure(TestCase):
    def setUp(self):
        if exists('./gg.ini'):
            copyfile('./gg.ini', './gg.ini.orig')

    def tearDown(self):
        if exists('./gg.ini'):
            remove('./gg.ini')
        if exists('./gg.ini.orig'):
            copyfile('./gg.ini.orig', './gg.ini')

    def test_configure_explicit(self):
        argv = ['--data-dir', TMPDIR, 'configure', '--name', NAME, '--roles', ROLES, '--keyid', KEYID,
                '--gnupg-home', GPGHOME, '--pass-manage', 'save', '--passphrase', 'gitguild']
        args = parser.parse_args(argv)
        configure(args=args)
        assert isfile('./gg.ini')
        ggini = ConfigParser()
        ggini.read('./gg.ini')
        assert ggini.get('me', 'name') == NAME
        assert ggini.get('me', 'roles') == ROLES.strip("\"")
        assert ggini.get('me', 'keyfp') == KEYID


class TestCharter(TestCase):
    def setUp(self):
        if exists(TMPDIR):
            rmtree(TMPDIR)
        self.repo = Repo.clone_from(EMPTYREPO, TMPDIR)

    # def tearDown(self):
    #     rmtree(TMPDIR)

    def test_charter_repo(self):
        argv = ['--data-dir', TMPDIR, 'charter', GGDATAREPO]
        args = parser.parse_args(argv)
        load_config(args)
        charter(args=args)
        assert exists(join(TMPDIR, '.git'))
        assert exists(join(TMPDIR, '.gg'))
        assert len(self.repo.submodules) == 1
        assert self.repo.submodules[0].module_exists()
        assert self.repo.submodules[0].module().working_tree_dir.endswith('.gg')
        assert basic_files_exist(args)

    # def test_charter_repo(self):
        argv2 = ['--data-dir', TMPDIR, '--overwrite', 'register']
        cli(argv2)
        assert exists(join(TMPDIR, '.gg', 'users', NAME))
        assert isfile(join(TMPDIR, '.gg', 'users', NAME, 'charter.md.asc'))
        assert isfile(join(TMPDIR, '.gg', 'users', NAME, 'maintainer.md.asc'))
        assert isfile(join(TMPDIR, '.gg', 'users', NAME, 'tester.md.asc'))
        # assert isfile(join(TMPDIR, '.gg', 'users', NAME, 'reporter.md.asc'))
        # assert False

        argv3 = ['--data-dir', TMPDIR, 'status']
        args3 = parser.parse_args(argv3)
        out = StringIO()
        status(args=args3, out=out)
        output = out.getvalue().strip()
        print output
        assert "WARNING" not in output
        assert "ERROR" not in output
