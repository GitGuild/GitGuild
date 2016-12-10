from os.path import join
from gitguild import repo

_members = {}


def members(refresh=True):
    if refresh or len(_members) == 0:
        authorpath = 'AUTHORS'
        with open(authorpath, 'r') as authorsf:
            for line in authorsf.readlines():
                line = line.strip()
                if len(line) == 0 or line.startswith("#"):
                    continue
                else:
                    memarray = line.split(" ")
                    _members[memarray[0]] = {'email': memarray[1], 'signingkey': memarray[2]}
            authorsf.close()
    return _members


def check_committer(commit):
    verification = repo.git.execute(['git', 'verify-commit', commit.hexsha], with_extended_output=True, with_exceptions=False)[2]
    assert "Good signature from " in verification
    assert str(commit.committer.name) in members()
    assert "key ID %s" % members()[commit.committer.name]['signingkey'] in verification
