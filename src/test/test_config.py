import StringIO
import argparse
from os import environ
from unittest import TestCase
from helpers import clean_testdir, cache_config, restore_cached_config, get_or_invent_config
from gitguild import get_user_name, get_user_email, get_user_signingkey, user_is_configured
from gitguild.command import config


class TestConfig(TestCase):
    def setUp(self):
        clean_testdir()
        cache_config(self)

    def tearDown(self):
        restore_cached_config(self)

    def test_config_fresh(self):
        assert not user_is_configured()
        try:
            assert get_user_name() is None
        except IOError as ge:
            assert ge.message == "Please configure a git user name by running 'git config --add user.name <name>'"
        try:
            assert get_user_email() is None
        except IOError as ge:
            assert ge.message == "Please configure a git user email by running 'git config --add user.email <email>'"
        try:
            assert get_user_signingkey() is None
        except IOError as ge:
            assert ge.message == "Please configure a git user signing key by running " \
                                 "'git config --add user.signingkey <signingkey>'"
        local_user_name, local_user_email, local_user_signingkey = get_or_invent_config(self)
        if environ and "GITGUILD_TEST_USER" in environ:
            assert " ".join([local_user_name, local_user_email, local_user_signingkey]) == environ["GITGUILD_TEST_USER"]
        assert user_is_configured()
        assert get_user_name() == local_user_name
        assert get_user_email() == local_user_email
        assert get_user_signingkey() == local_user_signingkey

    def test_config(self):
        out = StringIO.StringIO()
        args = argparse.Namespace()
        config(args, out=out)
        assert out.getvalue().strip() == "ERROR: Please configure a git user name by running " \
                                         "'git config --add user.name <name>'"
        out.close()
        # local_user_name, local_user_email, local_user_signingkey = get_or_invent_config(self)
        get_or_invent_config(self)
        newout = StringIO.StringIO()
        config(args, out=newout)
        assert newout.getvalue().strip() == ""
        # "Running as user: %s %s %s" % (local_user_name, local_user_email, local_user_signingkey)
        newout.close()
