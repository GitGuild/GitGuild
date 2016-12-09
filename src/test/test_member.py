from unittest import TestCase

from os.path import exists

from helpers import clean_testdir, get_transaction_path, cache_config, restore_cached_config, get_or_invent_config
from gitguild import basic_files_exist, repo


# class TestRegister(TestCase):
#     def setUp(self):
#         clean_testdir()
#         cache_config(self)
#
#     def tearDown(self):
#         restore_cached_config(self)
#
#     def test_register(self):
#         local_user_name, local_user_email, local_user_signingkey = get_or_invent_config(self)
#         guild = Guild.create_stub_guild(path=ABSDIR)
#         assert len(guild.members) == 0
#         guild.register()
#         assert len(guild.members) == 1
#         assert local_user_name in guild.members
#         assert len(guild.members[local_user_name]) == 2
#         assert guild.members[local_user_name]['email'] == local_user_email
#         assert guild.members[local_user_name]['signingkey'] == local_user_signingkey
#         with open(join(ABSDIR, 'AUTHORS'), 'r') as f:
#             assert "%s %s %s" % (local_user_name, local_user_email, local_user_signingkey) in f.read()
#             f.close()
#
#     def test_register_again(self):
#         local_user_name, local_user_email, local_user_signingkey = get_or_invent_config(self)
#         guild = Guild.create_stub_guild(path=ABSDIR)
#         assert len(guild.members) == 0
#         guild.register()
#         assert len(guild.members) == 1
#         assert local_user_name in guild.members
#         assert len(guild.members[local_user_name]) == 2
#         assert guild.members[local_user_name]['email'] == local_user_email
#         assert guild.members[local_user_name]['signingkey'] == local_user_signingkey
#         with open(join(ABSDIR, 'AUTHORS'), 'r') as f:
#             assert "%s %s %s" % (local_user_name, local_user_email, local_user_signingkey) in f.read()
#             f.close()
#
#     def test_register_duplicate_name(self):
#         local_user_name, local_user_email, local_user_signingkey = get_or_invent_config(self)
#         guild = Guild.create_stub_guild(path=ABSDIR)
#         assert len(guild.members) == 0
#         guild.register()
#         assert len(guild.members) == 1
#         assert local_user_name in guild.members
#         try:
#             guild.register()
#         except GuildError as ge:
#             assert ge.message == "User name %s already registered" % local_user_name
#
#     def test_register_duplicate_email(self):
#         local_user_name, local_user_email, local_user_signingkey = get_or_invent_config(self)
#         guild = Guild.create_stub_guild(path=ABSDIR)
#         assert len(guild.members) == 0
#         guild.register()
#         assert len(guild.members) == 1
#         assert local_user_name in guild.members
#         assert len(guild.members[local_user_name]) == 2
#         assert guild.members[local_user_name]['email'] == local_user_email
#         assert guild.members[local_user_name]['signingkey'] == local_user_signingkey
#         changed_user_name = "eve"
#         system('git config --local --unset-all user.name')
#         system('git config --local --add user.name %s' % changed_user_name)
#         guild._user_name = changed_user_name
#         try:
#             guild.register()
#         except GuildError as ge:
#             assert ge.message == "User email %s already registered" % local_user_email
#
#     def test_register_duplicate_signingkey(self):
#         local_user_name, local_user_email, local_user_signingkey = get_or_invent_config(self)
#         guild = Guild.create_stub_guild(path=ABSDIR)
#         assert len(guild.members) == 0
#         guild.register()
#         assert len(guild.members) == 1
#         assert local_user_name in guild.members
#         assert len(guild.members[local_user_name]) == 2
#         assert guild.members[local_user_name]['email'] == local_user_email
#         assert guild.members[local_user_name]['signingkey'] == local_user_signingkey
#         changed_user_name = "eve"
#         system('git config --local --unset-all user.name')
#         system('git config --local --add user.name %s' % changed_user_name)
#         guild._user_name = changed_user_name
#         changed_user_email = "eve@hax0r.com"
#         system('git config --local --unset-all user.email')
#         system('git config --local --add user.email %s' % changed_user_email)
#         guild._user_email = changed_user_email
#         try:
#             guild.register()
#         except GuildError as ge:
#             assert ge.message == "User signingkey %s already registered" % local_user_signingkey
#
#
