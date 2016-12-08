import ConfigParser
import argparse
import json
import sys
from os import makedirs, system
from os.path import exists, join, abspath

from gitguild import error, info, GuildError
from gitguild.types import Guild
from git.repo.base import InvalidGitRepositoryError

gpg = None
parser = argparse.ArgumentParser('gitguild')
subparsers = parser.add_subparsers(title='Commands', metavar='<command>')


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
parser.add_argument('--gg-path', default='./')


# Main entry point
def cli(argv=sys.argv[1:], out=sys.stdout):
    args = parser.parse_args(argv)
    args.func(args=args, out=out)


@command()
def init(args, out=sys.stdout):
    """Initialize new guild (create data files)"""
    try:
        guild = Guild.create_stub_guild(path=args.gg_path)
    except (IOError, GuildError, InvalidGitRepositoryError, AssertionError) as e:
        error(e.message, out=out)
        return
    info("created guild at %s" % args.gg_path, out=out)


@command()
def config(args, out=sys.stdout):
    """Configure git and gitguild for local use. i.e. set user name, email and signingkey"""
    try:
        guild = Guild(path=args.gg_path)
    except (IOError, GuildError, InvalidGitRepositoryError, AssertionError) as e:
        error(e.message, out=out)
        return
    try:
        guild.user_name
        guild.user_email
        guild.user_signingkey
    except GuildError as e:
        error(e.message, out=out)
        return


@command()
def register(args, out=sys.stdout):
    """Register with guild (update member file)"""
    guild = Guild(path=args.gg_path)
    try:
        guild.register()
        info('registered as member with name %s, key %s' % (guild.user_name, guild.user_signingkey), out=out)
    except (IOError, GuildError) as e:
        error("Unable to register for reason: %s" % e, out=out)


@command()
def status(args, out=sys.stdout):
    """Print report on guild and member status"""
    guild = Guild(path=args.gg_path)
    try:
        info(guild.guild_status(), out)
    except GuildError as ge:
        error(ge, out)
        return
    try:
        info(guild.member_status(), out)
    except GuildError as ge:
        error(ge, out)
        return


@command()
@cmd_arg('input_file', help='The file to create a schema stub for. This is the file that will be modified.')
@cmd_arg('title', help='The title json schema field.')
@cmd_arg('--can_be_guest', dest='member_required', action='store_false',
         help='If set, user need not be a member to make this change.')
@cmd_arg('--must_be_member', dest='member_required', action='store_true',
         help='If set, user must be a member to make this change.')  # default since second
@cmd_arg('--vote_percent_required', default='100', help='The percent of XP votes guild requires to accept this change.')
@cmd_arg('--description', help='The description json schema field.')
def make_schema_stub(args, out=sys.stdout):
    """Make a json schema stub for the file indicated."""
    path = abspath(args.gg_path)
    rawschema = {"diffbody": "",
                 "title": args.title,
                 "type": "object",
                 "must_be_member": args.member_required,
                 "vote_percent_required": float(args.vote_percent_required),
                 "properties": {
                 },
                 "required": []
                }
    if hasattr(args, 'description') and args.description is not None:
        rawschema['description'] = args.description
    with open(join(path, args.input_file), 'r') as f:
        rawschema['diffbody'] = f.read()
    outpath = join(path, "%s.json" % args.input_file)
    with open(outpath, 'w') as f:
        f.write(json.dumps(rawschema, indent=2))
        f.close()
    info("wrote %s" % outpath, out=out)


if __name__ == '__main__':
    cli()
