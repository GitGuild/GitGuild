from os.path import join
from unittest import TestCase
from helpers import clean_testdir, cache_config, restore_cached_config, get_transaction_path, get_or_invent_config, \
    prefill_init_params, prefill_init_templates
from gitguild import repo, create_stub_guild, basic_files_exist, commit
from gitguild.transaction import load_transaction, apply_transaction, get_param_list, param_chooser, \
    template_chooser, validate_transaction_diff


class TestTransactions(TestCase):
    def setUp(self):
        clean_testdir()
        cache_config(self)
        get_or_invent_config(self)

    def tearDown(self):
        restore_cached_config(self)

    def test_import_transactions(self):
        with open(".gitignore", 'w') as gi:
            gi.write("*~")
        repo.index.add(['.gitignore'])
        commit("gitignore")
        create_stub_guild(transaction_dir=get_transaction_path())
        assert repo.is_dirty()
        transaction = load_transaction('transaction_genesis')
        diffs = repo.head.commit.diff()
        validate_transaction_diff(transaction, diffs, plist={})

    def test_load_transaction(self):
        create_stub_guild(transaction_dir=get_transaction_path())
        transaction = load_transaction('init')
        assert transaction['title'] == 'init'

    def test_load_bad_transaction(self):
        tpath = get_transaction_path()
        create_stub_guild(transaction_dir=tpath)
        # modify and break some transaction
        with open(join('transaction', 'init.json'), 'r+b') as itf:
            contents = itf.read()
            itf.flush()
            itf.write(contents.replace('{', 'badjson'))
        self.assertRaises(ValueError, load_transaction, 'init')

    def test_load_non_existant_transaction(self):
        tpath = get_transaction_path()
        create_stub_guild(transaction_dir=tpath)
        self.assertRaises(IOError, load_transaction, 'aint')

    def test_get_param_list(self):
        create_stub_guild(transaction_dir=get_transaction_path())
        transaction = load_transaction('init')
        plist = get_param_list(transaction)
        assert isinstance(plist, list)

    def test_choose_param_list(self):
        prefill_init_params()
        create_stub_guild(transaction_dir=get_transaction_path())
        transaction = load_transaction('init')
        plist = get_param_list(transaction)
        assert isinstance(plist, list)
        invlist = {}
        i = 0
        for param in plist:
            invlist[param] = str(i)
            i += 1
        choices = param_chooser(plist)
        assert isinstance(choices, dict)
        assert len(choices) == len(plist)
        for param in plist:
            assert choices[param] == 'y'

    def test_choose_template_list(self):
        prefill_init_templates()
        create_stub_guild(transaction_dir=get_transaction_path())
        transaction = load_transaction('init')
        template_chooser(transaction)
        for category in transaction['files']:
            for tpl_cfg in transaction['files'][category]:
                if 'templates' in tpl_cfg:
                    assert len(tpl_cfg['templates']) <= 1

    def test_apply_transaction(self):
        prefill_init_templates()
        create_stub_guild(transaction_dir=get_transaction_path())
        commit("transaction genesis")
        transaction = load_transaction('init')
        template_chooser(transaction)
        prefill_init_params()
        plist = param_chooser(get_param_list(transaction))
        apply_transaction(transaction, plist=plist)
        diffs = repo.head.commit.diff()
        assert len(diffs) == len(transaction['files']["A"])
        assert basic_files_exist()
        assert repo.active_branch.name == 'voting'
        assert repo.is_dirty()

    def test_validate_transaction_diff(self):
        prefill_init_templates()
        create_stub_guild(transaction_dir=get_transaction_path())
        commit("transaction genesis")
        transaction = load_transaction('init')
        template_chooser(transaction)
        prefill_init_params()
        plist = param_chooser(get_param_list(transaction))
        apply_transaction(transaction, plist=plist)
        diffs = repo.head.commit.diff()
        validate_transaction_diff(transaction, diffs, plist=plist)

    def test_validate_transaction_diff_bad_param(self):
        prefill_init_templates()
        create_stub_guild(transaction_dir=get_transaction_path())
        commit("transaction genesis")
        transaction = load_transaction('init')
        template_chooser(transaction)
        prefill_init_params()
        plist = param_chooser(get_param_list(transaction))
        apply_transaction(transaction, plist=plist)
        diffs = repo.head.commit.diff()
        plist['years'] = '2016'
        self.assertRaises(AssertionError, validate_transaction_diff, transaction, diffs, plist=plist)

    def test_validate_transaction_diff_bad_template(self):
        prefill_init_templates()
        create_stub_guild(transaction_dir=get_transaction_path())
        commit("transaction genesis")
        transaction = load_transaction('init')
        template_chooser(transaction)
        prefill_init_params()
        plist = param_chooser(get_param_list(transaction))
        apply_transaction(transaction, plist=plist)
        tpath = join('transaction', 'CHANGELOG.md')
        with open(tpath, 'w') as cf:
            cf.write("changes hash bad!")
        repo.index.add([tpath])
        diffs = repo.head.commit.diff()
        self.assertRaises(AssertionError, validate_transaction_diff, transaction, diffs, plist=plist)

    def test_validate_transaction_diff_modify_more(self):
        prefill_init_templates()
        create_stub_guild(transaction_dir=get_transaction_path())
        commit("transaction genesis")
        transaction = load_transaction('init')
        template_chooser(transaction)
        prefill_init_params()
        plist = param_chooser(get_param_list(transaction))
        apply_transaction(transaction, plist=plist)
        npath = 'NEWFILE.md'
        with open(npath, 'w') as nf:
            nf.write("changes hash bad!")
        repo.index.add([npath])
        diffs = repo.head.commit.diff()
        self.assertRaises(AssertionError, validate_transaction_diff, transaction, diffs, plist=plist)

    def test_validate_transaction_diff_forget_file(self):
        prefill_init_templates()
        create_stub_guild(transaction_dir=get_transaction_path())
        commit("transaction genesis")
        transaction = load_transaction('init')
        template_chooser(transaction)
        prefill_init_params()
        plist = param_chooser(get_param_list(transaction))
        apply_transaction(transaction, plist=plist)
        repo.index.remove(['AUTHORS'])
        diffs = repo.head.commit.diff()
        self.assertRaises(AssertionError, validate_transaction_diff, transaction, diffs, plist=plist)
