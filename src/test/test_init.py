from os.path import exists
from unittest import TestCase

from gitguild import repo, create_stub_guild

from helpers import clean_testdir, get_transaction_path, cache_config, restore_cached_config, get_or_invent_config


class TestInit(TestCase):
    def setUp(self):
        clean_testdir()
        cache_config(self)
        get_or_invent_config(self)

    def tearDown(self):
        restore_cached_config(self)

    def test_import_transactions(self):
        create_stub_guild(transaction_dir=get_transaction_path())
        assert exists('transaction')
        assert repo.is_dirty()

    def test_import_no_transactions(self):
        try:
            create_stub_guild()
            assert "should have thrown an IOError" is None
        except IOError as e:
            assert e.message == "Either transaction_dir or transaction_repo must be specified to initialize guild."

    def test_import_transactions_full(self):
        tpath = get_transaction_path()
        create_stub_guild(transaction_dir=tpath)
        try:
            create_stub_guild(transaction_dir=tpath)
        except IOError as e:
            assert "couldn't copy transaction dir" in e.message
            return
        assert "should have thrown an exception" is None
