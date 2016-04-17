import click
import ConfigParser
import csv
import gnupg
import os
import pkgutil
import shutil
import sys

USERHOME = os.path.expanduser("~")
GGHOME = "%s/.gg" % USERHOME
if not os.path.exists(GGHOME):
    os.makedirs(GGHOME)

config = ConfigParser.ConfigParser()


@click.group()
@click.option('--data-dir', default='./.gg/', help='The path to the working guild data directory.')
@click.option('--overwrite/--no-overwrite', default=False)
@click.option('-g/-l', default=False, help='Use global (g) or local (l) configuration.')
@click.option('--gg-home', type=str, default=GGHOME, help='Where is the gg global config directory on your system? Default is ~/.gg')
@click.pass_context
def cli(ctx, data_dir, overwrite, g, gg_home):
    global GGHOME
    if gg_home != GGHOME:
        GGHOME = gg_home

    ctx.obj = {}
    ctx.obj['DATA_DIR'] = data_dir
    ctx.obj['OVERWRITE'] = overwrite
    ctx.obj['USEGLOBAL'] = g

    # load configuration
    if g:
        ctx.obj['CONFIG_PATH'] = get_config_path(ctx, 'global')
    else:
        ctx.obj['CONFIG_PATH'] = get_config_path(ctx)
    if ctx.obj['CONFIG_PATH'] is None or not os.path.isfile(ctx.obj['CONFIG_PATH']):
        click.echo("Looks like this gg instance is not configured.")
        click.echo("Running configuration command before continuing.\n")
        fname = ctx.invoke(configure)
        if fname is not None:
            ctx.obj['CONFIG_PATH'] = fname
        else:
            click.secho("ERROR: Unable to load gg configuration", fg='red', bold=True)
            sys.exit()
    config.read(ctx.obj['CONFIG_PATH'])
    set_ctx_gpg(ctx)


@cli.command()
@click.option('--name', type=str, prompt='What is your git username?')
@click.option('--role', type=str, prompt='What role will this user have?')
@click.option('--keyid', type=str, prompt='What pgp keyid will this user sign with?')
@click.option('--pass-manage', type=click.Choice(['agent', 'prompt', 'save']), default='prompt')
@click.option('--gnupg-home', type=str, prompt='Where is gnupg home on your system?')
@click.pass_context
def configure(ctx, name, role, keyid, pass_manage, gnupg_home):
    # prompt again in case invoking second hand...
    if name is None:
        name = click.prompt('What is your git username?', type=str)
    if role is None:
        role = click.prompt('What role will this user have?', type=str)
    if keyid is None:
        keyid = click.prompt('What pgp keyid will this user sign with?', type=str)
    if gnupg_home is None:
        gnupg_home = click.prompt('Where is gnupg home on your system?', type=str)

    set_ctx_gpg(ctx)
    skeys = ctx.obj['gpg'].list_keys(secret=True)
    foundskey = False
    for skey in skeys:
        if skey['keyid'].endswith(keyid):
            foundskey = True
    if not foundskey:
        click.secho("ERROR: No secret key found for keyid %s in gnupg-home %s" % (keyid, gnupg_home), fg='red', bold=True)
        return None

    fname = None
    if ctx.obj['USEGLOBAL']:
        fname = get_config_path(ctx, 'global')
    else:
        fname = get_config_path(ctx, 'local')

    if fname is not None and os.path.isfile(fname):
        if not ctx.obj['OVERWRITE']:
            click.echo("Found existing configuration. To overwrite, rerun using --overwrite.")
            return None
        else:
            os.remove(fname)

    with open(fname, 'w') as newconf:
        newconf.write("[me]\n")
        newconf.write("name: %s\n" % name)
        newconf.write("role: %s\n" % role)
        newconf.write("keyid: %s\n" % keyid)
        newconf.write("pass_manage: %s\n" % pass_manage)
        if pass_manage == 'save':
            password = click.prompt("Passphrase for keyid %s" % keyid, hide_input=True)
            newconf.write("passphrase: %s\n" % password)
        newconf.write("\n")
        newconf.write("[gpg]\n")
        newconf.write("homedir: %s\n" % gnupg_home)
        newconf.close()
    
    config.read(ctx.obj['CONFIG_PATH'])
    return fname


@cli.command()
@click.pass_context
@click.option('--template', default='software',  type=click.Choice(['software', 'medieval']), prompt='What charter template do you want to use?')
def charter(ctx, template):
    if os.path.exists(ctx.obj['DATA_DIR']):
        if ctx.obj['OVERWRITE']:
            click.echo('Overwriting guild in directory: %s' % ctx.obj['DATA_DIR'])
            shutil.rmtree(ctx.obj['DATA_DIR'])
        else:
            click.echo('Found existing guild in directory: %s' % ctx.obj['DATA_DIR'])
            click.echo('To overwrite, rerun using --overwrite.')
            return
    click.echo('Chartering new guild using template: %s' % template)

    os.makedirs(ctx.obj['DATA_DIR'])
    os.makedirs("%scontracts" % ctx.obj['DATA_DIR'])
    os.makedirs("%susers" % ctx.obj['DATA_DIR'])

    # write charter from template
    tempchart = pkgutil.get_data('gitguild', 'template/%s/charter.md' % template)
    with open("%scharter.md" % ctx.obj['DATA_DIR'], 'w') as f:
        f.write(tempchart) 
        f.close()
    lines = str(tempchart).split("\n")
    liststarted = False
    for line in lines:
        # read the roles lise out of the charter
        if "##### Roles List" in line:
            liststarted = True
            continue
        elif liststarted:
            if "#" in line:
                break
            elif "+" in line:
                role = line.strip(" +\n")
                tempcontract = pkgutil.get_data('gitguild', 'template/%s/contracts/%s.md' % (template, role))
                with open("%scontracts/%s.md" % (ctx.obj['DATA_DIR'], role), 'w') as f:
                    f.write(tempcontract) 
                    f.close()

    # create a roles.csv file
    with open("%sroles.csv" % ctx.obj['DATA_DIR'], 'w') as rolesfile:
        outcsv = csv.writer(rolesfile)
        outcsv.writerow(['Name', 'Role', 'Keyid', 'Status'])
        outcsv.writerow([config.get('me', 'name'),
                         config.get('me', 'role'),
                         config.get('me', 'keyid'),
                         'active'])

    # create a ledger.csv file
    with open("%sledger.csv" % ctx.obj['DATA_DIR'], 'w') as ledgerfile:
        outcsv = csv.writer(ledgerfile)
        outcsv.writerow(['Amount', 'Currency', 'txid', 'User', 'Reference'])

    # create your user directory and sign new documents
    userdir = "%susers/%s" % (ctx.obj['DATA_DIR'], config.get('me', 'name'))
    os.makedirs(userdir)
    passphrase = get_pass(ctx)
    sign_doc(ctx, 'charter', passphrase=passphrase)
    sign_doc(ctx, 'roles', passphrase=passphrase)
    sign_doc(ctx, 'ledger', passphrase=passphrase)
    sign_doc(ctx, "%scontracts/%s.md" % (ctx.obj['DATA_DIR'], config.get('me', 'role')), passphrase=passphrase)


@cli.command()
@click.pass_context
def status(ctx):
    if not basic_files_exist(ctx):
        click.echo("No valid guild data found.")
        return

    # check for user related file struture
    users = 0
    activeusers = 0
    rolespath = os.path.abspath("%sroles.csv" % ctx.obj['DATA_DIR'])
    rolesfile = open("%sroles.csv" % ctx.obj['DATA_DIR'], 'rb')
    charterpath = os.path.abspath("%scharter.md" % ctx.obj['DATA_DIR'])
    roles = csv.reader(rolesfile, delimiter=',')
    head = True
    for row in roles:
        if head:
            head = False
            continue
        users += 1
        if not os.path.exists("%susers/%s" % (ctx.obj['DATA_DIR'], row[0])):
            click.secho("WARNING: User %s has no directory" % row[0], fg='yellow')
            continue
        with open("%susers/%s/charter.md.asc" % (ctx.obj['DATA_DIR'], row[0]), 'rb') as chartsig:
            verified = ctx.obj['gpg'].verify_file(chartsig, charterpath)
            if not verified.valid:
                click.secho("WARNING: User %s did not sign the latest charter" % row[0], fg='yellow')
                continue
        sig_contract_path = os.path.abspath("%susers/%s/%s.md.asc" % (ctx.obj['DATA_DIR'], row[0], row[1]))
        with open(sig_contract_path, 'rb') as contractsig:
            contractpath = os.path.abspath("%scontracts/%s.md" % (ctx.obj['DATA_DIR'], row[1]))
            verified = ctx.obj['gpg'].verify_file(contractsig, contractpath)
            if not verified.valid:
                click.secho("WARNING: User %s did not sign the latest contract" % row[0], fg='yellow')
                continue
        activeusers += 1
    rolesfile.close()

    click.echo("Guild has %s users, %s of which are active" % (users, activeusers))

    

@cli.group()
@click.pass_context
def user(ctx):
    pass


@user.command()
@click.pass_context
def register(ctx):
    if not basic_files_exist(ctx):
        click.echo("No valid guild data found.")
        return

    updated = False
    isfirst = True
    shutil.copyfile("%sroles.csv" % ctx.obj['DATA_DIR'], "%sroles.csv.bak" % ctx.obj['DATA_DIR'])
    with open("%sroles.csv.bak" % ctx.obj['DATA_DIR'], 'rb') as rolesfile:
        roles = csv.reader(rolesfile, delimiter=',')
        with open("%sroles.csv" % ctx.obj['DATA_DIR'], 'wb') as newfile:
            newroles = csv.writer(newfile, delimiter=',')
            for row in roles:
                newroles.writerow(row)
                if isfirst:
                    isfirst = False
                    continue
                if row[0] == name:
                    if ctx.obj['OVERWRITE']:
                        click.echo("Overwriting user %s" % name)
                    else:
                        click.secho("WARNING: User %s exists. Use --overwrite to overwrite." % name, fg='yellow')
                        return
                    row[1] = role
                    row[2] = keyid
                    row[3] = 'pending'
                    updated = True
            if not updated:
                newroles.writerow([name, role, keyid, 'pending'])

    os.remove("%sroles.csv.bak" % ctx.obj['DATA_DIR'])

    userdir = "%susers/%s" % (ctx.obj['DATA_DIR'], config.get('me', 'name'))
    if not sys.path.exists(userdir):
        os.makedirs(userdir)

    sign_doc(ctx, 'charter')

    click.echo("registered user with name %s, role %s, keyid %s" % (name, role, keyid))


def get_config_path(ctx, location=None):
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
    if location == 'local' or (location is None and 
            os.path.isfile(localconfig)):
        return localconfig
    elif location == 'global' or (location is None and 
            os.path.isfile(globalconfig)):
        return globalconfig
    else:
        return None


def basic_files_exist(ctx):
    """
    Check for basic required file structure.
    """
    return (os.path.exists(ctx.obj['DATA_DIR']) and
         os.path.exists("%scontracts" % ctx.obj['DATA_DIR']) and
         os.path.exists("%susers" % ctx.obj['DATA_DIR']) and
         os.path.isfile("%scharter.md" % ctx.obj['DATA_DIR']) and
         os.path.isfile("%sroles.csv" % ctx.obj['DATA_DIR']))


def sign_doc(ctx, doc, passphrase=None):
    userdir = "%susers/%s" % (ctx.obj['DATA_DIR'], config.get('me', 'name'))
    if passphrase is None:
        passphrase = get_pass(ctx)

    if doc == 'charter':
        with open("%scharter.md" % ctx.obj['DATA_DIR'], 'rb') as charter:
            ctx.obj['gpg'].sign_file(charter, detach=True, keyid=config.get('me', 'keyid'), passphrase=passphrase, output="%s/charter.md.asc" % userdir)
    elif doc == 'roles':
        with open("%sroles.csv" % ctx.obj['DATA_DIR'], 'rb') as rolesfile:
            ctx.obj['gpg'].sign_file(rolesfile, detach=True, keyid=config.get('me', 'keyid'), passphrase=passphrase, output="%s/roles.csv.asc" % userdir)
    elif doc == 'ledger':
        with open("%sledger.csv" % ctx.obj['DATA_DIR'], 'rb') as ledgerfile:
            ctx.obj['gpg'].sign_file(ledgerfile, detach=True, keyid=config.get('me', 'keyid'), passphrase=passphrase, output="%s/ledger.csv.asc" % userdir)
    elif os.path.isfile(doc):
        with open(doc, 'rb') as f:
            fname = os.path.split(doc)[1]
            ctx.obj['gpg'].sign_file(f, detach=True, keyid=config.get('me', 'keyid'), passphrase=passphrase, output="%s/%s.asc" % (userdir, fname))
    else:
        raise IOError("Unable to sign doc %s" % doc)


def get_pass(ctx):
    if config.get('me', 'pass_manage') == 'prompt':
        return click.prompt("Passphrase for keyid %s" % config.get('me', 'keyid'), hide_input=True)
    elif config.get('me', 'pass_manage') == 'save' and config.get('me', 'passphrase') is not None:
        return config.get('me', 'passphrase')
    # for agent, let the agent gather it at runtime


def set_ctx_gpg(ctx):
    if 'gpg' in ctx.obj and isinstance(ctx.obj['gpg'], gnupg.GPG):
        return
    elif config.get('me', 'pass_manage') == "agent":
        ctx.obj['gpg'] = gnupg.GPG(gnupghome=config.get('gpg', 'homedir'), use_agent=True)
    else:
        ctx.obj['gpg'] = gnupg.GPG(gnupghome=config.get('gpg', 'homedir'))


if __name__ == '__main__':
    cli()

