from unittest import TestCase
from helpers import clean_testdir, get_transaction_path, cache_config, restore_cached_config, get_or_invent_config
from gitguild import basic_files_exist, repo, create_stub_guild, commit, ensure_members_unique
from gitguild.transaction import load_transaction, template_chooser, param_chooser, get_param_list, apply_transaction, \
    validate_transaction_diff


class TestRegister(TestCase):
    def setUp(self):
        clean_testdir()
        cache_config(self)
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

    def tearDown(self):
        restore_cached_config(self)

    def test_register(self):
        reg_trans = load_transaction('register')
        template_chooser(reg_trans, prompt=False)
        reg_plist = param_chooser('register', get_param_list(reg_trans), prompt=False)
        apply_transaction(reg_trans, plist=reg_plist)
        reg_diffs = repo.head.commit.diff()
        validate_transaction_diff(reg_trans, reg_diffs, plist=reg_plist)
        ensure_members_unique()

    def test_register_bad_format(self):
        reg_trans = load_transaction('register')
        template_chooser(reg_trans, prompt=False)
        reg_plist = param_chooser('register', get_param_list(reg_trans), prompt=False)
        apply_transaction(reg_trans, plist=reg_plist)
        with open('AUTHORS', 'r') as af:
            lines = af.readlines()
        with open('AUTHORS', 'w') as af:
            lines[-1] = lines[-1].replace(" ", ", ")
            af.writelines(lines)
        repo.index.add(['AUTHORS'])
        reg_diffs = repo.head.commit.diff()
        self.assertRaises(AssertionError, validate_transaction_diff, reg_trans, reg_diffs, plist=reg_plist)

    def test_register_duplicate_name(self):
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

    def test_register_duplicate_email(self):
        with open('AUTHORS', 'w') as af:
            af.write("%s %s %s\n" % (self.user_name + "a", self.user_email, self.user_signingkey + "a"))
        repo.index.add(['AUTHORS'])
        commit('previous registration')
        reg_trans = load_transaction('register')
        template_chooser(reg_trans, prompt=False)
        reg_plist = param_chooser('register', get_param_list(reg_trans), prompt=False)
        apply_transaction(reg_trans, plist=reg_plist)
        reg_diffs = repo.head.commit.diff()
        self.assertRaises(AssertionError, ensure_members_unique)
        validate_transaction_diff(reg_trans, reg_diffs, plist=reg_plist)

    def test_register_duplicate_signingkey(self):
        with open('AUTHORS', 'w') as af:
            af.write("%s %s %s\n" % (self.user_name + "a", self.user_email + "a", self.user_signingkey))
        repo.index.add(['AUTHORS'])
        commit('previous registration')
        reg_trans = load_transaction('register')
        template_chooser(reg_trans, prompt=False)
        reg_plist = param_chooser('register', get_param_list(reg_trans), prompt=False)
        apply_transaction(reg_trans, plist=reg_plist)
        reg_diffs = repo.head.commit.diff()
        self.assertRaises(AssertionError, ensure_members_unique)
        validate_transaction_diff(reg_trans, reg_diffs, plist=reg_plist)
