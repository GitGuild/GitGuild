import datetime
import sys
from os import chdir

from gitguild import cmd_arg, command, error, info, parser, get_user_name, get_user_email, get_user_signingkey, \
    create_stub_guild, basic_files_exist, ensure_members_unique
from gitguild.transaction import load_transaction, apply_transaction, template_chooser, get_param_list, param_chooser


def cli(argv=sys.argv[1:], out=sys.stdout):
    args = parser.parse_args(argv)
    if hasattr(args, 'gg_path') and args.gg_path is not None:
        chdir(args.gg_path)
    args.func(args=args, out=out)


@command()
def config(args, out=sys.stdout):
    """Configure git and gitguild for local use. i.e. get user name, email and signingkey"""
    try:
        # info("Running as user: %s %s %s" % (get_user_name(), get_user_email(), get_user_signingkey()), out)
        "Running as user: %s %s %s" % (get_user_name(), get_user_email(), get_user_signingkey())
    except IOError as e:
        error(e.message, out=out)
        return


@command()
@cmd_arg('--years', help='The years that the copyright is active for.')
@cmd_arg('--authors', default="AUTHORS", help='The authors of the copyright material.')
# @cmd_arg('--license', default="MIT", choices=["MIT", "CC4"], help='The intellectual property license to use.')
def init(args, out=sys.stdout):
    """Initialize local guild (create data files)"""
    config(args, out=out)
    if args.years is None or len(args.years) == 0:
        args.years = str(datetime.date.today().year)
    try:
        transaction = load_transaction('init')
        template_chooser(transaction)
        apply_transaction(transaction, plist={'LICENSE': {'years': args.years, 'authors': args.authors}})
    except IOError as e:
        error(e.message, out=out)
        return
    info("created guild", out=out)


@command()
@cmd_arg('--transaction_dir', help='The local directory with transaction templates to seed this guild.')
@cmd_arg('--transaction_repo', help='The remote git repo with transaction templates to seed this guild.')
@cmd_arg('--transaction_repo_branch', default='master',
         help='The remote git repo branch with transaction templates to seed this guild.')
def import_transactions(args, out=sys.stdout):
    """Import transactions from a local directory or git repository."""
    config(args, out=out)
    try:
        create_stub_guild(transaction_dir=args.transaction_dir, transaction_repo=args.transaction_repo,
                          transaction_repo_branch=args.transaction_repo_branch)
    except IOError as e:
        error(e.message, out=out)
        return
    info("imported transactions", out=out)


@command()
def status(args, out=sys.stdout):
    """Print report on guild and member status"""
    try:
        basic_files_exist()
        ensure_members_unique()
        info("Guild in good standing.", out)
    except AssertionError as e:
        error(str(e), out)



@command()
def register(args, out=sys.stdout):
    """Register with guild (update member file)"""
    config(args, out=out)
    try:
        transaction = load_transaction('register')
        template_chooser(transaction)
        plist = param_chooser(get_param_list(transaction))
        apply_transaction(transaction, plist=plist)
    except IOError as e:
        error(e.message, out=out)
        return
    info("created guild", out=out)
