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
