from os.path import join


def members(path):
    _members = {}
    authorpath = join(path, 'AUTHORS')
    with open(authorpath, 'r') as authorsf:
        for line in authorsf.readlines():
            line = line.strip()
            if len(line) == 0 or line.startswith("#"):
                continue
            else:
                memarray = line.split(" ")
                _members[memarray[0]] = {'email': memarray[1], 'signingkey': str(memarray[2:])}
        authorsf.close()
    return _members


# def register(path):
#
#     if self.user_name in self.members:
#         raise GuildError("User name %s already registered" % self.user_name)
#     mempath = join(self.path, 'AUTHORS')
#     with open(mempath, 'r+b') as memf:
#         wfile = memf.read()
#         if " %s " % self.user_email in wfile:  # TODO pretty inefficient query method
#             memf.close()
#             raise GuildError("User email %s already registered" % self.user_email)
#         elif " %s\n" % self.user_signingkey in wfile:  # TODO pretty inefficient query method
#             memf.close()
#             raise GuildError("User signingkey %s already registered" % self.user_signingkey)
#         else:
#             memf.write("%s %s %s\n" % (self.user_name, self.user_email, self.user_signingkey))
#             self._members[self.user_name] = {'email': self.user_email, 'signingkey': self.user_signingkey}
#         memf.close()
#
#
# def member_status(self, name=None):
#     name = name if name is not None else self.user_name
#     ismember = True if name in self.members else False
#     isuser = True if name == self.user_name else False
#
#     if ismember and isuser:
#         return "%s is one of the %s members" % (name, len(self.members))
#     else:
#         current = "current " if isuser else ""
#         memnot = " not" if not ismember else ""
#         raise GuildError("%s%s is%s one of the %s members" % (current, name, memnot, len(self.members)))
#
#
# @command()
# def register(args, out=sys.stdout):
#     """Register with guild (update member file)"""
#     path = abspath(args.gg_path)
#     if not basic_files_exist(path):
#         error("No valid guild data found.", out)
#         return
#
#     try:
#         guild.register()
#         info('registered as member with name %s, key %s' % (guild.user_name, guild.user_signingkey), out=out)
#     except (IOError, GuildError) as e:
#         error("Unable to register for reason: %s" % e, out=out)
