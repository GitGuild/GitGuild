from argparse import Namespace
from unittest import TestCase

from StringIO import StringIO

from helpers import clean_testdir, get_transaction_path, cache_config, restore_cached_config, get_or_invent_config
from gitguild import basic_files_exist, repo, create_stub_guild, commit, ensure_members_unique
from gitguild.command import status
from gitguild.transaction import load_transaction, template_chooser, param_chooser, apply_transaction, \
    validate_transaction_diff, get_param_list


class TestStatus(TestCase):
    def setUp(self):
        clean_testdir()
        cache_config(self)

    def tearDown(self):
        restore_cached_config(self)

    def test_status_good(self):
        get_or_invent_config(self)
        create_stub_guild(transaction_dir=get_transaction_path())
        self.user_name, self.user_email, self.user_signingkey = get_or_invent_config(self)
        commit("transaction genesis")
        transaction = load_transaction('init')
        template_chooser(transaction, prompt=False)
        plist = param_chooser('init', get_param_list(transaction), prompt=False)
        apply_transaction(transaction, plist=plist)
        diffs = repo.head.commit.diff()
        validate_transaction_diff(transaction, diffs, plist=plist)
        commit("initialize")
        output = StringIO()
        status(object, output)
        assert output.getvalue().strip() == """valid 'init' transaction for last commit
Guild in good standing."""

    def test_status_duplicate_user(self):
        get_or_invent_config(self)
        create_stub_guild(transaction_dir=get_transaction_path())
        self.user_name, self.user_email, self.user_signingkey = get_or_invent_config(self)
        commit("transaction genesis")
        transaction = load_transaction('init')
        template_chooser(transaction, prompt=False)
        plist = param_chooser('init', get_param_list(transaction), prompt=False)
        apply_transaction(transaction, plist=plist)
        diffs = repo.head.commit.diff()
        validate_transaction_diff(transaction, diffs, plist=plist)
        commit("initialize")
        with open('AUTHORS', 'w') as af:
            af.write("%s %s %s\n" % (self.user_name, self.user_email + "a", self.user_signingkey + "a"))
        repo.index.add(['AUTHORS'])
        commit('previous registration')
        reg_trans = load_transaction('register')
        template_chooser(reg_trans, prompt=False)
        reg_plist = param_chooser('register', get_param_list(reg_trans), prompt=False)
        apply_transaction(reg_trans, plist=reg_plist)
        reg_diffs = repo.head.commit.diff()
        self.assertRaises(AssertionError, ensure_members_unique)
        validate_transaction_diff(reg_trans, reg_diffs, plist=reg_plist)
        output = StringIO()
        status(object, output)
        # TODO change this expectation to something friendlier
        assert output.getvalue().strip() == "ERROR: assert '{0}' not in ['{0}']".format(self.user_name)

    def test_status_uncommitted_transaction(self):
        get_or_invent_config(self)
        create_stub_guild(transaction_dir=get_transaction_path())
        self.user_name, self.user_email, self.user_signingkey = get_or_invent_config(self)
        commit("transaction genesis")
        transaction = load_transaction('init')
        template_chooser(transaction, prompt=False)
        plist = param_chooser('init', get_param_list(transaction), prompt=False)
        apply_transaction(transaction, plist=plist)
        diffs = repo.head.commit.diff()
        validate_transaction_diff(transaction, diffs, plist=plist)
        commit("initialize")
        reg_trans = load_transaction('register')
        template_chooser(reg_trans, prompt=False)
        reg_plist = param_chooser('register', get_param_list(reg_trans), prompt=False)
        apply_transaction(reg_trans, plist=reg_plist)
        output = StringIO()
        status(object, output)
        print output.getvalue().strip()
        assert output.getvalue().strip() == """WARNING: valid 'register' transaction waiting commit
valid 'init' transaction for last commit
Guild in good standing."""

    def test_status_bad_uncommitted_transaction(self):
        get_or_invent_config(self)
        create_stub_guild(transaction_dir=get_transaction_path())
        self.user_name, self.user_email, self.user_signingkey = get_or_invent_config(self)
        commit("transaction genesis")
        transaction = load_transaction('init')
        template_chooser(transaction, prompt=False)
        plist = param_chooser('init', get_param_list(transaction), prompt=False)
        apply_transaction(transaction, plist=plist)
        diffs = repo.head.commit.diff()
        validate_transaction_diff(transaction, diffs, plist=plist)
        commit("initialize")
        with open('AUTHORS', 'w') as af:
            af.write("%s %s %s\n" % (self.user_name, self.user_email + "a", self.user_signingkey + "a"))
        repo.index.add(['AUTHORS'])
        commit('previous registration')
        reg_trans = load_transaction('register')
        template_chooser(reg_trans, prompt=False)
        reg_plist = param_chooser('register', get_param_list(reg_trans), prompt=False)
        apply_transaction(reg_trans, plist=reg_plist)
        output = StringIO()
        status(object, output)
        assert output.getvalue().strip() == "ERROR: assert '{0}' not in ['{0}']".format(self.user_name)

    def test_status_depth(self):
        get_or_invent_config(self)
        create_stub_guild(transaction_dir=get_transaction_path())
        self.user_name, self.user_email, self.user_signingkey = get_or_invent_config(self)
        commit("transaction genesis")
        transaction = load_transaction('init')
        template_chooser(transaction, prompt=False)
        plist = param_chooser('init', get_param_list(transaction), prompt=False)
        apply_transaction(transaction, plist=plist)
        diffs = repo.head.commit.diff()
        validate_transaction_diff(transaction, diffs, plist=plist)
        commit("initialize")
        reg_trans = load_transaction('register')
        template_chooser(reg_trans, prompt=False)
        reg_plist = param_chooser('register', get_param_list(reg_trans), prompt=False)
        apply_transaction(reg_trans, plist=reg_plist)
        output = StringIO()
        status(object, output)
        assert output.getvalue().strip() == """WARNING: valid 'register' transaction waiting commit
valid 'init' transaction for last commit
Guild in good standing."""
        commit("register")
        output = StringIO()
        args = Namespace()
        args.depth = 2
        status(args, output)
        assert output.getvalue().strip() == """valid 'register' transaction for last commit
valid 'init' transaction for previous commit
Guild in good standing."""
        output = StringIO()
        args = Namespace()
        args.depth = 3
        status(args, output)
        assert output.getvalue().strip() == """valid 'register' transaction for last commit
valid 'init' transaction for previous commit
reached the root of the git tree
Guild in good standing."""

    def test_status_wrong_user_register(self):
        get_or_invent_config(self)
        create_stub_guild(transaction_dir=get_transaction_path())
        self.user_name, self.user_email, self.user_signingkey = get_or_invent_config(self)
        commit("transaction genesis")
        transaction = load_transaction('init')
        template_chooser(transaction, prompt=False)
        plist = param_chooser('init', get_param_list(transaction), prompt=False)
        apply_transaction(transaction, plist=plist)
        diffs = repo.head.commit.diff()
        validate_transaction_diff(transaction, diffs, plist=plist)
        commit("initialize")
        reg_trans = load_transaction('register')
        template_chooser(reg_trans, prompt=False)
        reg_plist = param_chooser('register', get_param_list(reg_trans), prompt=False)
        apply_transaction(reg_trans, plist=reg_plist)
        #overwrite
        with open('AUTHORS', 'w') as af:
            af.write("isysd ira@gitguild.com 5C3586F6")
        repo.index.add(['AUTHORS'])
        output = StringIO()
        status(object, output)
        outval = output.getvalue().strip()
        assert "ERROR: assert" in outval

    def test_status_wrong_signer(self):
        get_or_invent_config(self)
        create_stub_guild(transaction_dir=get_transaction_path())
        self.user_name, self.user_email, self.user_signingkey = get_or_invent_config(self)
        commit("transaction genesis")
        transaction = load_transaction('init')
        template_chooser(transaction, prompt=False)
        plist = param_chooser('init', get_param_list(transaction), prompt=False)
        apply_transaction(transaction, plist=plist)
        diffs = repo.head.commit.diff()
        validate_transaction_diff(transaction, diffs, plist=plist)
        commit("initialize")
        reg_trans = load_transaction('register')
        template_chooser(reg_trans, prompt=False)
        reg_plist = param_chooser('register', get_param_list(reg_trans), prompt=False)
        apply_transaction(reg_trans, plist=reg_plist)
        output = StringIO()
        status(object, output)
        outval = output.getvalue().strip()
        assert output.getvalue().strip() == """WARNING: valid 'register' transaction waiting commit
valid 'init' transaction for last commit
Guild in good standing."""
        # overwrite
        with open('AUTHORS', 'w') as af:
            af.write("isysd ira@gitguild.com 5C3586F6")
        repo.index.add(['AUTHORS'])
        commit("register")
        output = StringIO()
        args = Namespace()
        args.depth = 2
        status(args, output)
        assert "ERROR: assert" in output.getvalue().strip()

    def test_status_no_signature(self):
        get_or_invent_config(self)
        create_stub_guild(transaction_dir=get_transaction_path())
        self.user_name, self.user_email, self.user_signingkey = get_or_invent_config(self)
        commit("transaction genesis")
        transaction = load_transaction('init')
        template_chooser(transaction, prompt=False)
        plist = param_chooser('init', get_param_list(transaction), prompt=False)
        apply_transaction(transaction, plist=plist)
        diffs = repo.head.commit.diff()
        validate_transaction_diff(transaction, diffs, plist=plist)
        commit("initialize")
        reg_trans = load_transaction('register')
        template_chooser(reg_trans, prompt=False)
        reg_plist = param_chooser('register', get_param_list(reg_trans), prompt=False)
        apply_transaction(reg_trans, plist=reg_plist)
        output = StringIO()
        status(object, output)
        assert output.getvalue().strip() == """WARNING: valid 'register' transaction waiting commit
valid 'init' transaction for last commit
Guild in good standing."""
        repo.index.commit("register")
        output = StringIO()
        args = Namespace()
        args.depth = 2
        status(args, output)
        assert output.getvalue().strip() == """ERROR: assert 'Good signature from ' in ''"""
