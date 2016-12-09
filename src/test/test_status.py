from unittest import TestCase
from helpers import clean_testdir, get_transaction_path, cache_config, restore_cached_config, get_or_invent_config
from gitguild import basic_files_exist, repo

# class TestStatus(TestCase):
#     def setUp(self):
#         clean_testdir()
#         cache_config(self)
#
#     def tearDown(self):
#         restore_cached_config(self)
#
#     def test_status_empty(self):
#         guild = Guild.create_stub_guild(path=ABSDIR)
#         clean_testdir()
#         try:
#             guild_status = guild.guild_status()
#             assert "should not hit this line" is False
#         except GuildError as ge:
#             assert ge.message == "Not currently in a guild. Run 'init' command to create one."
#
#     def test_status_good(self):
#         local_user_name, local_user_email, local_user_signingkey = get_or_invent_config(self)
#         guild = Guild.create_stub_guild(path=ABSDIR)
#         try:
#             guild.member_status(local_user_name)
#             assert "should not hit this line" is False
#         except GuildError as ge:
#             assert ge.message == "current %s is not one of the 0 members" % local_user_name
#         try:
#             guild.member_status('username')
#             assert "should not hit this line" is False
#         except GuildError as ge:
#             assert ge.message == "username is not one of the 0 members"
#         guild.register()
#         guild_status = guild.guild_status()
#         assert guild_status == "Guild in good standing."
#         member_status = guild.member_status()
#         assert member_status == "%s is one of the 1 members" % local_user_name
