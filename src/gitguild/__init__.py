import argparse
import subprocess
import sys
from os.path import exists, isfile, abspath
from shutil import Error
from shutil import copytree

from git import Repo, InvalidGitRepositoryError, GitCommandError

parser = argparse.ArgumentParser('gitguild')
subparsers = parser.add_subparsers(title='Commands', metavar='<command>')
repo = None

try:
    repo = Repo()
except InvalidGitRepositoryError:
    sys.exit("gitguild must be run from within an initialized git repository.")


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


# Output helpers
def error(msg, out=sys.stdout):
    """Print an error message"""
    out.write('ERROR: %s\n' % msg)


def warning(msg, out=sys.stdout):
    """Print a warning message"""
    out.write('WARNING: %s\n' % msg)


def info(msg, out=sys.stdout):
    """Print an informational message"""
    out.write('%s\n' % msg)


def create_stub_guild(transaction_dir=None, transaction_repo=None, transaction_repo_branch='master'):
    global repo
    # copy transaction templates
    if transaction_dir is not None:
        # transaction templates are in a local directory
        tpath = abspath(transaction_dir)
        if not exists(tpath):
            raise IOError("%s does not exist" % tpath)
        else:
            try:
                copytree(tpath, "transaction")
            except (Error, OSError):
                raise IOError("couldn't copy transaction dir %s to transaction" % tpath)
    elif transaction_repo is not None:
        # transaction templates are in a remote repo, create submodule
        repo = Repo()
        repo.create_submodule("transaction", "transaction", url=transaction_repo,
                              branch=transaction_repo_branch)
    else:
        raise IOError("Either transaction_dir or transaction_repo must be specified to initialize guild.")
    repo.index.add(["transaction"])
    # repo.index.commit("imported transactions")


def basic_files_exist():
    """
    Check for basic required file structure.
    """
    return (exists('transaction') and
            isfile('AUTHORS') and
            isfile('CHANGELOG.md') and
            isfile('CONTRIBUTING.md'))


def get_user_name():
    """
    Get the current user's name from git config.

    :raises IOError: If there is an error getting the config value
    :return: The git config user.name value
    """
    try:
        return subprocess.check_output(['git', 'config', 'user.name']).strip()
    except subprocess.CalledProcessError:
        raise IOError("Please configure a git user name by running 'git config --add user.name <name>'")


def get_user_email():
    """
    Get the current user's email from git config.

    :raises IOError: If there is an error getting the config value
    :return: The git config user.email value
    """
    try:
        return subprocess.check_output(['git', 'config', 'user.email']).strip()
    except subprocess.CalledProcessError:
        raise IOError("Please configure a git user email by running 'git config --add user.email <email>'")


def get_user_signingkey():
    """
    Get the current user's GnuPG signing key from git config.

    :raises IOError: If there is an error getting the config value
    :return: The git config user.signingkey value
    """
    try:
        return subprocess.check_output(['git', 'config', 'user.signingkey']).strip()
    except subprocess.CalledProcessError:
        raise IOError("Please configure a git user signing key by running "
                      "'git config --add user.signingkey <signingkey>'")


def user_is_configured():
    """
    Return True if the current user is configured properly, else False.

    :rtype: bool
    """
    try:
        get_user_name()
        get_user_email()
        get_user_signingkey()
        return True
    except IOError:
        return False


def commit(message):
    try:
        repo.git.checkout(b="voting")
    except GitCommandError:
        pass
    repo.git.commit("-S", "-m", message)
