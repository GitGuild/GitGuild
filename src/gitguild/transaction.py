import json
from os import makedirs, system
from os.path import join, isfile

from gitguild import repo


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


def param_chooser(plist):
    # Parameters are gathered for the whole transaction to avoid duplication
    if len(plist) == 0:
        return {}
    print "Configuring parameters for %s" % plist
    choices = {}
    for param in plist:
        print "Please enter a value for %s" % param
        choices[param] = raw_input()
    print "You chose the following parameters\n'%s'\nIs that correct? (y/n)" % choices
    if raw_input() not in 'yYesyes':
        print("Better start over.")
        param_chooser(plist)
    return choices


def replace_parameters(template, plist):
    for param in plist:
        template = template.replace('[%s]' % param, str(plist[param]))
    return template


def template_chooser(transaction):
    # templates only apply to files
    for category in transaction['files']:
        for out_name in transaction['files'][category]:
            tpl_cfg = transaction['files'][category][out_name]
            if 'templates' in tpl_cfg and len(tpl_cfg['templates']) > 1:
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


def validate_transaction_diffs_type(transaction, diffs, plist, dcopy, ctype="A"):
    cdiffs = list(diffs.iter_change_type(ctype))
    tfcopy = transaction['files'][ctype].copy()
    for diff in cdiffs:
        # file out name should be in files list
        assert diff.b_rawpath in transaction['files'][ctype]
        # check contents
        with open(diff.b_rawpath, 'r') as bf:
            b_content = bf.read()
        try:
            a_content = diff.a_blob.data_stream.read()
        except AttributeError:
            a_content = ""
        if 'templates' not in transaction['files'][ctype][diff.b_rawpath] or \
            len(transaction['files'][ctype][diff.b_rawpath]['templates']) == 0:
            dcopy.remove(diff)
            del tfcopy[diff.b_rawpath]
        else:
            for tpl_name in transaction['files'][ctype][diff.b_rawpath]['templates']:
                with open(transaction['files'][ctype][diff.b_rawpath]['templates'][tpl_name], 'r') as tplf:
                    tpl = replace_parameters(tplf.read(), plist)
                if ctype == "A":
                    validate_add_file(tpl, a_content, b_content)
                elif ctype == "M":
                    validate_mod_file(tpl, a_content, b_content, method="append")
                elif ctype == "D":
                    validate_del_file(tpl, a_content, b_content)
                dcopy.remove(diff)
                del tfcopy[diff.b_rawpath]
    assert len(tfcopy) == 0


def validate_transaction_diff(transaction, diffs, plist=None):
    # Validate by elimination. This diffs copy should be empty at the end.
    dcopy = diffs[:]
    validate_transaction_diffs_type(transaction, diffs, plist, dcopy, ctype="A")
    validate_transaction_diffs_type(transaction, diffs, plist, dcopy, ctype="M")
    validate_transaction_diffs_type(transaction, diffs, plist, dcopy, ctype="D")
    validate_transaction_diffs_type(transaction, diffs, plist, dcopy, ctype="R")
    assert len(dcopy) == 0
