import json
from os import makedirs, system
from os.path import join, isfile

import datetime

import sys
from gitguild import repo


def load_transaction(transName):
    """
    Load a transaction from the active guild's transaction directory.

    :raises IOError: If the transaction config file could not be found.
    :raises ValueError: If the transaction config file was not a valid document.
    :param str transName: The name of the transaction, i.e. the config name before .json
    """
    transPath = join("transaction", "%s.json" % transName)
    if not isfile(transPath):
        raise IOError("Unknown transaction type %s" % transName)
    with open(transPath, 'r') as tf:
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


def apply_template(out_name, tfile, plist):
    # assume index 0 is chosen template
    if not isfile(tfile):
        raise IOError("Unable to find template file %s" % tfile)
    else:
        with open(tfile, 'r') as tplfile:
            template = replace_parameters(tplfile.read(), plist)
        with open(out_name, 'w') as outfile:
            outfile.write(template)


def apply_transaction(transaction, plist=None):
    for newdir in transaction['directories']['new']:
        makedirs(newdir)
        repo.index.add([newdir])
    for out_name in transaction['files']['new']:
        newfile = transaction['files']['new'][out_name]
        if isfile(out_name):
            raise IOError("Output file name already exists. Will not overwrite.")
        elif "templates" in newfile and len(newfile["templates"]) == 1:
            apply_template(out_name, newfile['templates'][newfile['templates'].keys()[0]], plist)
        elif "templates" in newfile:
            # this shouldn't happen if you already ran template chooser
            apply_template(out_name, newfile, plist)
        else:
            system("touch %s" % out_name)
        repo.index.add([out_name])


def validate_transaction_diff(transaction, diffs, plist=None):
    # Validate by elimination. This diffs copy should be empty at the end.
    dcopy = diffs[:]
    adds = list(diffs.iter_change_type('A'))
    assert len(transaction['files']['new']) == len(adds)
    for diff in adds:
        assert diff.new_file
        # file out name should be in new files list
        assert diff.b_rawpath in transaction['files']['new']
        # check contents
        with open(diff.b_rawpath, 'r') as bf:
            b_content = bf.read().strip()
            if 'templates' in transaction['files']['new'][diff.b_rawpath]:
                for tpl_name in transaction['files']['new'][diff.b_rawpath]['templates']:
                    with open(transaction['files']['new'][diff.b_rawpath]['templates'][tpl_name], 'r') as tplf:
                        a_content = replace_parameters(tplf.read().strip(), plist)
                        if a_content == b_content:
                            dcopy.remove(diff)
            else:
                assert b_content == ""
                dcopy.remove(diff)
    assert len(dcopy) == 0
