import __builtin__
from git import GitCommandError, Repo
from os import remove, chdir, makedirs, walk, environ
from os.path import exists, join, abspath, dirname, realpath
from shutil import rmtree

EMPTYREPO = 'https://github.com/GitGuild/empty_repo.git'
if 'GITGUILD_TEST_REPO' in environ:
    EMPTYREPO = environ['GITGUILD_TEST_REPO']
TESTDIR = environ['GITGUILD_TEST_DIR'] if 'GITGUILD_TEST_DIR' in environ else '/tmp/ggtest'
ABSDIR = abspath(TESTDIR)
if not exists(ABSDIR):
    makedirs(ABSDIR)
chdir(ABSDIR)


def get_or_invent_config(testcase):
    if 'GITGUILD_TEST_USER' in environ:
        local_user_name, local_user_email, local_user_signingkey = environ['GITGUILD_TEST_USER'].split(" ")
    else:
        local_user_name = 'troll4u'
        local_user_email = 'troll4u@gitguild.com'
        local_user_signingkey = '69F7F1A6'
        if testcase.global_user_name is not None:
            local_user_name = testcase.global_user_name
        if testcase.global_user_email is not None:
            local_user_name = testcase.global_user_email
        if testcase.global_user_signingkey is not None:
            local_user_signingkey = testcase.global_user_signingkey
    repo.git.config('user.name', '%s' % local_user_name, local=True, add=True)
    repo.git.config('user.email', '%s' % local_user_email, local=True, add=True)
    repo.git.config('user.signingkey', '%s' % local_user_signingkey, local=True, add=True)
    return local_user_name, local_user_email, local_user_signingkey


def clean_testdir():
    global repo
    for root, dirs, files in walk(ABSDIR):
        for name in files:
            remove(join(root, name))
        for name in dirs:
            rmtree(join(root, name), ignore_errors=True)
    repo = Repo.init()


def cache_config(testcase):
    try:
        testcase.global_user_name = repo.git.config('--global', 'user.name')
        repo.git.config('--global', '--unset-all', 'user.name')
    except GitCommandError:
        testcase.global_user_name = None
    try:
        testcase.global_user_email = repo.git.config('--global', 'user.email')
        repo.git.config('--global', '--unset-all', 'user.email')
    except GitCommandError:
        testcase.global_user_email = None
    try:
        testcase.global_user_signingkey = repo.git.config('--global', 'user.signingkey')
        repo.git.config('--global', '--unset-all', 'user.signingkey')
    except GitCommandError:
        testcase.global_user_signingkey = None


def restore_cached_config(testcase):
    if testcase.global_user_email is not None and len(testcase.global_user_email) > 0:
        repo.git.config('--global', 'user.email', '%s' % testcase.global_user_email, add=True)
    if testcase.global_user_name is not None and len(testcase.global_user_name) > 0:
        repo.git.config('--global', 'user.name', '%s' % testcase.global_user_name, add=True)
    if testcase.global_user_signingkey is not None and len(testcase.global_user_signingkey) > 0:
        repo.git.config('--global', 'user.signingkey', '%s' % testcase.global_user_signingkey, add=True)
    try:
        repo.git.config('--unset-all', 'user.name', local=True)
        repo.git.config('--unset-all', 'user.email', local=True)
        repo.git.config('--unset-all', 'user.signingkey', local=True)
    except GitCommandError:
        pass


def get_transaction_path():
    # create new guild using the transactions from this one
    testpath = dirname(realpath(__file__))
    return testpath.replace("src/test", "transaction")


input_responses = ['y']
lastresp = 0


# noinspection PyUnusedLocal
def raw_input(prompt=None):
    """
    Override built-in input function for testing. Respond with next string from input_responses list, or start over.

    :param prompt: ignored
    :return: 'y'
    """
    global lastresp
    resp = input_responses[lastresp]
    lastresp += 1
    if lastresp >= len(input_responses):
        lastresp = 0
    return resp
__builtin__.raw_input = raw_input


def reset_responses():
    global lastresp
    lastresp = 0
    del input_responses[:]


def prefill_init_templates():
    reset_responses()
    input_responses.append('MIT')


def prefill_init_params():
    reset_responses()
    input_responses.append('y')
