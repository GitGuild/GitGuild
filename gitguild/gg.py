import ConfigParser
import argparse
import sys
from os import makedirs, system
from os.path import exists, join

from gitguild import error, info, gitname, gitsigkey
from gitguild.types import Guild

config = ConfigParser.ConfigParser()
gpg = None
parser = argparse.ArgumentParser('gg')
subparsers = parser.add_subparsers(title='Commands', metavar='<command>')

# def repo(self):
#     if self._repo is None:
#         self._repo = Repo(self.root)
#     return self._repo


# def add_gg_repo(gg_repo, args, branch='master'):
#     if args.gg_path is None:
#         args.gg_path = "./"
#     Submodule.add(guild.repo, 'gg', guild.args.gg_path, gg_repo, branch=branch)


class Command(object):
    """
    Temporary object to accumulate subcommand arguments (to be passed between
    the below decorators, not used directly)
    """

    def __init__(self, func):
        self.func = func
        self.args = []


def command(name=None, **kwargs):
    """
    Declare a subcommand, adding it and any arguments from cmd_arg() to the
    parser. Use as the outermost (first) decorator. Decorator keyword arguments
    are passed through to add_parser() and thus include any ArgumentParser
    constructor arguments, plus "help", which defaults to the function's
    docstring.
    """

    def decorator(cmd):
        if not isinstance(cmd, Command):
            cmd = Command(cmd)
        func = cmd.func
        cmd_name = name if name is not None else func.__name__
        if 'help' not in kwargs and func.__doc__ is not None:
            kwargs['help'] = func.__doc__
        subparser = subparsers.add_parser(cmd_name, **kwargs)
        subparser.set_defaults(func=func)
        for arg_args, arg_kwargs in reversed(cmd.args):
            subparser.add_argument(*arg_args, **arg_kwargs)
        return func

    return decorator


def cmd_arg(*args, **kwargs):
    """
    Declare a subcommand argument. Use zero or more of these inside (below) a
    command() decorator; they will be ordered top to bottom. Decorator
    arguments are passed through to ArgumentParser.add_argument().
    """

    def decorator(cmd):
        if not isinstance(cmd, Command):
            cmd = Command(cmd)
        cmd.args.append((args, kwargs))
        return cmd

    return decorator


# Global args
parser.add_argument('--overwrite', action='store_false')
parser.add_argument('--gg-path', default='./')


# Main entry point
def cli(argv=sys.argv[1:], out=sys.stdout):
    args = parser.parse_args(argv)
    args.func(args=args, out=out)


@command()
@cmd_arg('--fork-votes', default=100, help='Percent of XP votes required to fork (rebase) this guild.')
@cmd_arg('--charter-votes', default=90, help='Percent of XP votes required to change the charter.')
@cmd_arg('--sidechain-votes', default=75, help='Percent of XP votes required to create or update a sidechain.')
@cmd_arg('--agreement-votes', default=66, help='Percent of XP votes required to make a guild-wide agreement.')
@cmd_arg('--member-votes', default=51, help='Percent of XP votes required to become a member.')
def init(args, out=sys.stdout):
    """Charter new guild (create data files, sign charter)"""
    vote_table = {'fork': args.fork_votes,
                  'charter': args.charter_votes,
                  'sidechain': args.sidechain_votes,
                  'agreement': args.agreement_votes,
                  'member': args.member_votes}
    guild = Guild.create_stub_guild(path=args.gg_path, vote_table=vote_table)
    guild.register()
    guild.approve_member(gitname)
    # create_stub_guild(args=args)


@command()
def register(args, out=sys.stdout):
    """Register with guild (update member file, make vote account)"""
    guild = Guild(path=args.gg_path)
    try:
        guild.register()
        info('registered as member with name %s, key %s' % (gitname, gitsigkey), out=out)
    except IOError as e:
        error("Unable to register for reason: %s" % e, out=out)

# Sub-commands
# @command()
# @cmd_arg('giturl', help='The git repository to use for your guild. '
#                         'Should be a clean or pre-populated with your guild data.')
# def add(args, out=sys.stdout):
#     """Add an existing guild (link submodule)"""
#     if exists(join(args.data_dir, '.gg')):
#         if args.overwrite:
#             info('Overwriting guild in directory: %s' % args.data_dir, out=out)
#             shutil.rmtree(args.data_dir)
#         else:
#             info('Found existing guild in directory: %s' % args.data_dir, out=out)
#             info('To overwrite, rerun using --overwrite.', out=out)
#             return
#
#     gg_repo = args.ggrepo
#     if gg_repo is not None:
#         info('Chartering new guild using gg_repo: %s' % gg_repo, out=out)
#         Guild.create_from_gg_repo(gg_repo=gg_repo, path=args.data_dir, branch='ledger')
#     else:
#         warning('Guilds should only be chartered from existing data repositories for now.', out=out)
#         # return
#         info('Creating new guild stub', out=out)
#         Guild.create_stub_guild(args.data_dir)
#
#
# @command()
# def status(args, out=sys.stdout):
#     """Check document signatures and report on guild status"""
#
#     if not basic_files_exist(args):
#         error('No valid guild data found.', out=out)
#         return
#
#     # check for user related file structure
#     users = 0
#     activeusers = 0
#     with open(_data_file('members.csv'), 'rb') as membersfile:
#         members = csv.reader(membersfile, delimiter=',')
#         head = True
#         for row in members:
#             if head:
#                 head = False
#                 continue
#             users += 1
#             user = row[0]
#             roles = row[1].split()
#             if not exists(_data_file('users/%s' % user)):
#                 warning('User %s has no directory' % user, out=out)
#                 continue
#             all_valid = True
#             with open(_data_file('users/%s/charter.md.asc' % user), 'rb') as chartsig:
#                 charterpath = _data_file('charter.md')
#                 verified = gpg.verify_file(chartsig, charterpath)
#                 if not verified.valid:
#                     warning('User %s did not sign the latest charter' % user, out=out)
#                     all_valid = False
#             if all_valid:
#                 activeusers += 1
#
#     info('Guild has %s users, %s of which are active' % (users, activeusers), out=out)


# @command()
# def task(args, out=sys.stdout):
#     """Create a task entry in the ledger. Should correspond to an existing repository issue on github."""
#     if not basic_files_exist(args):
#         error('No valid guild data found.', out=out)
#         return
#     with open(data_file(args, 'ledger.dat'), 'w') as ledgerfile:
#         pass


if __name__ == '__main__':
    cli()

