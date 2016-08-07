import argparse
import getpass
import ConfigParser
import csv
import gnupg
import os
import shutil
import sys
import copy
from functools import partial

from git import Repo, Submodule

GGHOME = os.path.expanduser('~/.gg')
if not os.path.exists(GGHOME):
    os.makedirs(GGHOME)

config = ConfigParser.ConfigParser()
gpg = None
parser = argparse.ArgumentParser('gg')
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


def error(msg, out=sys.stdout):
    """Print an error message"""
    out.write('ERROR: %s' % msg)


def warning(msg, out=sys.stdout):
    """Print a warning message"""
    out.write('WARNING: %s' % msg)


def info(msg, out=sys.stdout):
    """Print an informational message"""
    out.write(msg)


def data_file(args, path):
    """Qualify a gg file/directory path based on the --data-dir argument"""
    return os.path.join(args.data_dir, '.gg', path)


def load_config(args, out=sys.stdout):
    config_path = get_config_path('global' if args.global_ else None)
    if config_path is None or not os.path.isfile(config_path):
        info('Looks like this gg instance is not configured.', out=out)
        info('Running configuration command before continuing.\n', out=out)
        tmp_args = parser.parse_args(['configure'], copy.copy(args))
        fname = configure(tmp_args)
        if fname is not None:
            config_path = fname
        else:
            error('Unable to load gg configuration')
            return
    config.read(config_path)
    # basic config validation
    for section in ('me', 'gpg'):
        if not config.has_section(section):
            error('Invalid config %s: missing section "%s"' % (config_path, section), out=out)
            return
    if config.has_option('me', 'role'):
        if config.has_option('me', 'roles'):
            warning('Ignoring deprecated "role" in %s' % config_path, out=out)
        else:
            warning('"role" is deprecated in %s, please rename to "roles"' % config_path, out=out)
            config.set('me', 'roles', config.get('me', 'role'))

# Global args
parser.add_argument('--data-dir', default='./',
                    help='The path to the working repository. Assumed to be CWD.')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--global', action='store_true', dest='global_',
                    help='Force global configuration. (Normally, config will '
                         'be read from the current directory, falling back to the '
                         'global directory if not found there, and generated '
                         'config will be written to the current directory.)')
parser.add_argument('--gg-home', default=GGHOME, help='Where is the gg global '
                                                      'config directory on your system? Default is ~/.gg')


# Main entry point
def cli(argv=sys.argv[1:], out=sys.stdout):
    args = parser.parse_args(argv)
    global GGHOME
    if args.gg_home != GGHOME:
        GGHOME = args.gg_home

    if args.func is configure:
        configure(args, out=out)
        return

    # load configuration
    load_config(args, out=out)

    global gpg
    gpg = gnupg.GPG(
        gnupghome=config.get('gpg', 'homedir'),
        use_agent=(config.get('me', 'pass_manage') == 'agent'))

    args.func(args, out=out)


# Subcommands

@command()
@cmd_arg('--name')
@cmd_arg('--roles')
@cmd_arg('--keyid')
@cmd_arg('--pass-manage', choices=['agent', 'prompt', 'save'], default='prompt')
@cmd_arg('--passphrase', help="Use this to save your passphrase permanently. Not safe!")
@cmd_arg('--gnupg-home')
def configure(args, out=sys.stdout):
    """Initialize new gg.ini"""

    def get_arg(parameter, prompt):
        arg = getattr(args, parameter)
        if arg is None:
            arg = raw_input(prompt)
        return arg

    name = get_arg('name', 'What is your git username? ')
    roles = get_arg('roles', 'What role(s) will this user have? (space separated) ').strip("\"").strip("'").split()
    keyid = get_arg('keyid', 'What pgp keyid/fingerprint will this user sign with? ')
    gnupg_home = get_arg('gnupg_home', 'Where is gnupg home on your system? ')
    pass_manage = args.pass_manage

    keyid = collapse_fprint(keyid.upper())
    gnupg_home = os.path.expanduser(gnupg_home)
    gpg = gnupg.GPG(gnupghome=gnupg_home, use_agent=(pass_manage == 'agent'))
    skeys = gpg.list_keys(secret=True)
    fprint = None
    for skey in skeys:
        if skey['fingerprint'].endswith(keyid):
            if fprint is not None:
                error('Multiple secret keys found matching %s. '
                      'Try using a full fingerprint.' % keyid, out=out)
                return None
            fprint = skey['fingerprint']
    if fprint is None:
        error('No secret key found for keyid %s in gnupg-home %s' % (keyid, gnupg_home), out=out)
        return None

    fname = get_config_path('global' if args.global_ else 'local')

    if fname is not None and os.path.isfile(fname):
        if not args.overwrite:
            info('Found existing configuration. To overwrite, rerun using --overwrite.', out=out)
            return None
        else:
            os.remove(fname)

    with open(fname, 'w') as newconf:
        newconf.write("[me]\n")
        newconf.write("name: %s\n" % name)
        newconf.write("roles: %s\n" % ' '.join(roles))
        newconf.write("keyfp: %s\n" % fprint)
        newconf.write("pass_manage: %s\n" % pass_manage)
        if pass_manage == 'save':
            password = getpass.getpass("Passphrase for keyid %s: " % fprint)
            newconf.write("passphrase: %s\n" % password)
        newconf.write("\n")
        newconf.write("[gpg]\n")
        newconf.write("homedir: %s\n" % gnupg_home)
        newconf.close()

    return fname


@command()
@cmd_arg('ggdata', help='The git data repository to use as a charter template. '
                        'Should be a clean or pre-populated Git Guild data repository.')
def charter(args, out=sys.stdout):
    """Charter new guild (create data files, sign contracts)"""

    _data_file = partial(data_file, args)

    if os.path.exists(os.path.join(args.data_dir, '.gg')):
        if args.overwrite:
            info('Overwriting guild in directory: %s' % args.data_dir, out=out)
            shutil.rmtree(args.data_dir)
        else:
            info('Found existing guild in directory: %s' % args.data_dir, out=out)
            info('To overwrite, rerun using --overwrite.', out=out)
            return

    repo = Repo(args.data_dir)

    gg_data = args.ggdata
    if gg_data is not None:
        info('Chartering new guild using gg_data: %s' % gg_data, out=out)
        Submodule.add(repo, 'gg', os.path.join(args.data_dir, '.gg'), gg_data, branch='ledger')
    else:
        warning('Guilds can only be chartered from existing data repositories for now.', out=out)
        return
        # info('Creating new guild stub', out=out)
        # os.makedirs(os.path.join(args.data_dir, '.gg'))
        # os.makedirs(_data_file('contracts'))
        # os.makedirs(_data_file('users'))
        # with open(_data_file('charter.md'), 'w') as charterfile:
        #     charterfile.write("# GitGuild Charter Stub")
        #     charterfile.write("Write your own charter here")
        #     charterfile.close()
        #
        # with open(_data_file('members.csv'), 'w') as memberfile:
        #     memberfile.write("Name, Roles, Keyid, Status")
        #     memberfile.close()
        #
        # with open(_data_file('ledger.dat'), 'w') as ledgerfile:
        #     ledgerfile.write("; automatically generated ledger stub")
        #     ledgerfile.close()

    # create your user directory and sign new documents
    # userdir = _data_file('users/%s' % config.get('me', 'name'))
    # os.makedirs(userdir)
    # passphrase = get_pass()
    # sign_doc(args, 'charter.md', passphrase=passphrase)
    # sign_doc(args, 'members.csv', passphrase=passphrase)
    # sign_doc(args, 'ledger.csv', passphrase=passphrase)
    # for role in config.get('me', 'roles').split():
    #     sign_doc(args, 'contracts/%s.md' % role, passphrase=passphrase)


@command()
def status(args, out=sys.stdout):
    """Check contract signatures and report on guild status"""

    if not basic_files_exist(args):
        error('No valid guild data found.', out=out)
        return

    _data_file = partial(data_file, args)

    # check for user related file structure
    users = 0
    activeusers = 0
    with open(_data_file('members.csv'), 'rb') as membersfile:
        members = csv.reader(membersfile, delimiter=',')
        head = True
        for row in members:
            if head:
                head = False
                continue
            users += 1
            user = row[0]
            roles = row[1].split()
            if not os.path.exists(_data_file('users/%s' % user)):
                warning('User %s has no directory' % user, out=out)
                continue
            all_valid = True
            with open(_data_file('users/%s/charter.md.asc' % user), 'rb') as chartsig:
                charterpath = os.path.abspath(_data_file('charter.md'))
                verified = gpg.verify_file(chartsig, charterpath)
                if not verified.valid:
                    warning('User %s did not sign the latest charter' % user, out=out)
                    all_valid = False
            for role in roles:
                with open(_data_file('users/%s/%s.md.asc' % (user, role)), 'rb') as contractsig:
                    contractpath = os.path.abspath(_data_file('contracts/%s.md' % role))
                    verified = gpg.verify_file(contractsig, contractpath)
                    if not verified.valid:
                        warning('User %s did not sign the latest %s contract' % (user, role), out=out)
                        all_valid = False
            if all_valid:
                activeusers += 1

    info('Guild has %s users, %s of which are active' % (users, activeusers), out=out)


@command()
def register(args, out=sys.stdout):
    """Register with guild (update members.csv, sign charter)"""

    if not basic_files_exist(args):
        error('No valid guild data found.', out=out)
        return

    name = config.get('me', 'name')
    roles = config.get('me', 'roles').split()
    keyfp = config.get('me', 'keyfp')
    new_row = [name, ' '.join(roles), keyfp, 'pending']

    members_path = data_file(args, 'members.csv')
    new_path = data_file(args, '._members.csv.new')
    with open(members_path, 'rb') as membersfile:
        members = csv.reader(membersfile, delimiter=',')
        new_file = open(new_path, 'wb')
        try:
            newmembers = csv.writer(new_file, delimiter=',')
            updated = False
            isfirst = True
            for row in members:
                if isfirst:  # Skip header
                    isfirst = False
                elif len(row) > 0 and row[0] == name:
                    if not args.overwrite:
                        error('User %s exists. Use --overwrite to overwrite.' % name, out=out)
                        return
                    if updated:
                        warning('Dropping duplicate entry for user %s' % name, out=out)
                        continue
                    info('Overwriting user %s' % name, out=out)
                    row = new_row
                    updated = True
                newmembers.writerow(row)
            if not updated:
                newmembers.writerow(new_row)
            os.fdatasync(new_file.fileno())
            new_file.close()
            os.rename(new_path, members_path)
        finally:
            new_file.close()
            if os.path.exists(new_path):
                os.remove(new_path)

    userdir = data_file(args, 'users/%s' % name)
    if not os.path.exists(userdir):
        os.makedirs(userdir)

    passphrase = get_pass()
    sign_doc(args, 'charter.md', passphrase=passphrase)
    for role in roles:
        sign_doc(args, 'contracts/%s.md' % role, passphrase=passphrase)

    info('registered user with name %s, roles (%s), key %s' % (name, ' '.join(roles), keyfp), out=out)


def get_config_path(location=None):
    """
    Find the chosen or most relevant configuration for this session.
    Filename is expected to be 'gg.ini' regardless of location.

    Order of preference:

    1. current working directory
    2. $HOME/.gg/
    """
    fname = "gg.ini"
    localconfig = "./%s" % fname
    globalconfig = "%s/%s" % (GGHOME, fname)
    if location == 'local':
        return localconfig
    elif location == 'global':
        return globalconfig
    elif location is None:
        if os.path.isfile(localconfig):
            return localconfig
        elif os.path.isfile(globalconfig):
            return globalconfig
        else:
            return None
    else:
        raise ValueError("Invalid location %r" % location)


def basic_files_exist(args):
    """
    Check for basic required file structure.
    """
    _data_file = partial(data_file, args)
    return (os.path.exists(args.data_dir) and
            os.path.exists(_data_file('contracts')) and
            os.path.exists(_data_file('users')) and
            os.path.isfile(_data_file('charter.md')) and
            os.path.isfile(_data_file('members.csv')))


def sign_doc(args, doc, passphrase=None):
    userdir = data_file(args, 'users/%s' % config.get('me', 'name'))
    if passphrase is None:
        passphrase = get_pass()

    fname = os.path.split(doc)[1]
    output = "%s/%s.asc" % (userdir, fname)
    with open(data_file(args, doc), 'rb') as f:
        sig = gpg.sign_file(f, detach=True, keyid=config.get('me', 'keyfp'), passphrase=passphrase)
        with open(output, 'w') as out:
            out.write(str(sig))
            out.close()


def get_pass():
    if config.get('me', 'pass_manage') == 'prompt':
        return getpass.getpass("Passphrase for keyid %s: " % config.get('me', 'keyfp'))
    elif config.get('me', 'pass_manage') == 'save':
        return config.get('me', 'passphrase')
        # for agent, let the agent gather it at runtime


def collapse_fprint(fprint):
    return ''.join(fprint.split(' '))


def expand_fprint(fprint):
    if len(fprint) != 40:
        raise ValueError('Invalid collapsed fingerprint')

    def group(string, grpsize):
        return [string[i:i + grpsize] for i in range(0, len(string), grpsize)]

    return '  '.join(' '.join(group(s, 4)) for s in group(fprint, 20))


if __name__ == '__main__':
    cli()
