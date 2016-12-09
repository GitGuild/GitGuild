import sys
from gitguild import command, info, error, basic_files_exist
from os.path import abspath


@command()
def status(args, out=sys.stdout):
    """Print report on guild and member status"""
    path = abspath(args.gg_path)
    if not basic_files_exist(path):
        error("Not currently in a guild. Run 'init' command to create one.", out)
    else:
        info("Guild in good standing.", out)

        # try:
        #     info(member_status(path), out)
        # except IOError as ge:
        #     error(ge, out)
        #     return
