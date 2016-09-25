import subprocess
import sys

gitname = subprocess.check_output(['git', 'config', 'user.name']).strip()
gitsigkey = subprocess.check_output(['git', 'config', 'user.signingkey']).strip()


def error(msg, out=sys.stdout):
    """Print an error message"""
    out.write('ERROR: %s\n' % msg)


def warning(msg, out=sys.stdout):
    """Print a warning message"""
    out.write('WARNING: %s\n' % msg)


def info(msg, out=sys.stdout):
    """Print an informational message"""
    out.write('%s\n' % msg)
