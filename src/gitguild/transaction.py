import json
from os import makedirs, system
from os.path import join, isfile

import datetime
from time import strftime, gmtime

from gitguild import repo, get_user_name, get_user_email, get_user_signingkey
from gitguild.member import members


def load_transaction(tname):
    """
    Load a transaction from the active guild's transaction directory.

    :raises IOError: If the transaction config file could not be found.
    :raises ValueError: If the transaction config file was not a valid document.
    :param str tname: The name of the transaction, i.e. the config name before .json
    """
    tpath = join("transaction", "%s.json" % tname)
    if not isfile(tpath):
        raise IOError("Unknown transaction type %s" % tname)
    with open(tpath, 'r') as tf:
        transaction = json.loads(tf.read())
    return transaction


def get_param_list(transaction):
    plist = []
    for category in transaction['files']:
        for out_name in transaction['files'][category]:
            tpl = transaction['files'][category][out_name]
            if 'parameters' in tpl and len(tpl['parameters']) > 0:
                for param in tpl['parameters']:
                    plist.append(param)
    return plist


def param_chooser(tname, plist, commit=None, prompt=True):
    # Parameters are gathered for the whole transaction to avoid duplication
    if len(plist) == 0:
        return {}
    choices = {}
    if prompt:
        print "Configuring parameters for %s" % plist
        for param in plist:
            print "Please enter a value for %s" % param
            choices[param] = raw_input()
        print "You chose the following parameters\n'%s'\nIs that correct? (y/n)" % choices
        if raw_input() not in 'yYesyes' and prompt:
            print("Better start over.")
            param_chooser(tname, plist, prompt=prompt)
    elif tname == "register":
        if commit is None:
            choices['user_name'] = get_user_name().strip()
            choices['user_email'] = get_user_email()
            choices['user_signingkey'] = get_user_signingkey()
        else:
            choices['user_name'] = commit.committer.name.strip()
            choices['user_email'] = commit.committer.email
            choices['user_signingkey'] = members()[commit.committer.name]['signingkey']
    elif tname == "init":
        if commit is None:
            choices['years'] = str(datetime.date.today().year)
        else:
            choices['years'] = strftime('%Y', gmtime(commit.committed_date))
        choices['AUTHORS'] = "AUTHORS"
    return choices


def replace_parameters(template, plist):
    for param in plist:
        template = template.replace('[%s]' % param, str(plist[param]))
    return template


def template_chooser(transaction, commit=None, prompt=True):
    # templates only apply to files
    for category in transaction['files']:
        for out_name in transaction['files'][category]:
            tpl_cfg = transaction['files'][category][out_name]
            if 'templates' in tpl_cfg and len(tpl_cfg['templates']) > 1:
                if prompt:
                    print("Please choose a template for %s" % out_name)
                    for template in tpl_cfg['templates']:
                        print("%s\t%s" % (template, tpl_cfg['templates'][template]))
                    tkeys = tpl_cfg['templates'].keys()
                    print("Which template do you choose? %s (%s)" % (tkeys, tkeys[0]))
                    choice = raw_input()
                    if choice not in tkeys:
                        raise IOError("Choice %s not understood. Options were %s" % (choice, tkeys))
                    else:
                        tpl_cfg['templates'] = {choice: tpl_cfg['templates'][choice]}
                elif transaction['title'] == "init" and commit is None:
                    transaction['files']['A']['LICENSE']['templates'] = {'MIT':
                         transaction['files']['A']['LICENSE']['templates']['MIT']}
                elif transaction['title'] == "init":
                    with open("LICENSE", 'r') as lic:
                        if 'MIT License' in lic.readline():
                            choice = 'MIT'
                        else:
                            choice = 'CC4'
                    transaction['files']['A']['LICENSE']['templates'] = {choice:
                         transaction['files']['A']['LICENSE']['templates'][choice]}
    print transaction['files']['A']


def apply_template(out_name, tfile, plist, method="A"):
    if not isfile(tfile):
        raise IOError("Unable to find template file %s" % tfile)
    with open(tfile, 'r') as tplfile:
        template = replace_parameters(tplfile.read(), plist)
    if method == "A":
        with open(out_name, 'w') as outfile:
            outfile.write(template)
    elif not isfile(out_name):
            raise IOError("Unable to find expected file %s" % out_name)
    elif method == "append":
        with open(out_name, "a") as outfile:
            outfile.write(template)


def apply_transaction(transaction, plist=None):
    for newdir in transaction['directories']["A"]:
        makedirs(newdir)
        repo.index.add([newdir])
    for out_name in transaction['files']["A"]:
        newfile = transaction['files']["A"][out_name]
        if isfile(out_name):
            raise IOError("Output file name already exists. Will not overwrite.")
        elif "templates" in newfile and len(newfile["templates"]) >= 1:
            apply_template(out_name, newfile['templates'][newfile['templates'].keys()[0]], plist)
        else:
            system("touch %s" % out_name)
        repo.index.add([out_name])
    for out_name in transaction['files']["M"]:
        if transaction['files']["M"][out_name]["method"] == "append":
            tpls = transaction['files']["M"][out_name]['templates']
            tpl = tpls[tpls.keys()[0]]
            apply_template(out_name, tpl, plist, method="append")
        repo.index.add([out_name])
    with open('.transaction', 'w') as wf:
        wf.write(transaction["title"])
    try:
        repo.index.add(['.transaction'])
    except Exception as e:
        print e


def validate_add_file(tpl, a_content, b_content, method=None):
    assert a_content == ""
    assert tpl == b_content


def validate_del_file(tpl, a_content, b_content, method=None):
    assert b_content == ""


def validate_mod_file(tpl, a_content, b_content, method="append"):
    if method == "append":
        validate_append_file(tpl, a_content, b_content)


def validate_append_file(tpl, a_content, b_content):
    assert b_content == a_content + tpl


def validate_transaction_diffs_type(transaction, diffs, plist, dcopy=None, ctype="A"):
    # print transaction
    cdiffs = list(diffs.iter_change_type(ctype))
    tfcopy = transaction['files'][ctype].copy()
    for diff in cdiffs:
        try:
            b_content = diff.b_blob.data_stream.read()
        except AttributeError:
            b_content = ""
        # print "b_content '%s'" % b_content[:10]
        if diff.b_rawpath == '.transaction':
            assert b_content == transaction['title']
            if dcopy is not None:
                dcopy.remove(diff)
            continue
        # file out name should be in files list
        assert diff.b_rawpath in transaction['files'][ctype]
        # check contents
        try:
            a_content = diff.a_blob.data_stream.read()
        except AttributeError:
            a_content = ""
        # print "a_content '%s'" % a_content[:10]
        if 'templates' not in transaction['files'][ctype][diff.b_rawpath] or \
                len(transaction['files'][ctype][diff.b_rawpath]['templates']) == 0:
            del tfcopy[diff.b_rawpath]
            if dcopy is not None:
                dcopy.remove(diff)
        else:
            for tpl_name in transaction['files'][ctype][diff.b_rawpath]['templates']:
                with open(transaction['files'][ctype][diff.b_rawpath]['templates'][tpl_name], 'r') as tplf:
                    tpl = replace_parameters(tplf.read(), plist)
                # print "'%s' =? '%s' < '%s'" % (b_content[:10], a_content[:10], tpl[:10])
                if ctype == "A":
                    validate_add_file(tpl, a_content, b_content)
                elif ctype == "M":
                    validate_mod_file(tpl, a_content, b_content, method="append")
                elif ctype == "D":
                    validate_del_file(tpl, a_content, b_content)
                if dcopy is not None:
                    dcopy.remove(diff)
                del tfcopy[diff.b_rawpath]
    # print "tfcopy %s" % tfcopy
    assert len(tfcopy) == 0


def validate_transaction_diff(transaction, diffs, plist=None):
    # Validate by elimination. This diffs copy should be empty at the end.
    dcopy = list(diffs)[:]
    validate_transaction_diffs_type(transaction, diffs, plist, dcopy, ctype="A")
    validate_transaction_diffs_type(transaction, diffs, plist, dcopy, ctype="M")
    validate_transaction_diffs_type(transaction, diffs, plist, dcopy, ctype="D")
    validate_transaction_diffs_type(transaction, diffs, plist, dcopy, ctype="R")
    assert len(dcopy) == 0


def get_diff_file_list(diffs):
    flist = []
    for diff in list(diffs):
        flist.append(diff.b_rawpath)
    return flist
