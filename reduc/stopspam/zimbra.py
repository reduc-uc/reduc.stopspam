import sh
from commandr import command

from reduc.stopspam import config


ZMPROV = config.get('shell', 'zmprov')
ZIMBRA_SERVER = config.get('zimbra', 'server')


@command('zimbra-suspend', category='zimbra')
def zimbra_suspend(ids):
    """Suspends zimbra accounts separates by comma."""
    ids = ids.split(',')
    for id in ids:
        suspend(id)


@command('zimbra-reactivate', category='zimbra')
def zimbra_reactivate(ids):
    """Reactivates zimbra accounts separated by comma."""
    ids = ids.split(',')
    for id in ids:
        reactivate(id)


@command('zimbra-status', category='zimbra')
def zimbra_status(ids):
    """Prints status of zimbra accounts separated by comma."""
    ids = ids.split(',')
    for id in ids:
        stat = status(id)
        print '{0}: {1}, {2}'.format(id, stat[0], stat[1])


def suspend(id):
    """Suspends a zimbra account."""
    cmd_zmprov_ma(id, 'zimbraAccountStatus', 'locked')
    cmd_zmprov_ma(id, 'zimbraMailStatus', 'disabled')


def reactivate(id):
    """Reactivates a zimbra account."""
    cmd_zmprov_ma(id, 'zimbraAccountStatus', 'active')
    cmd_zmprov_ma(id, 'zimbraMailStatus', 'enabled')


def status(id):
    """Gets the status of an account account."""
    accountStatus = cmd_zmprov_ga(id, 'zimbraAccountStatus')
    mailStatus = cmd_zmprov_ga(id, 'zimbraMailStatus')
    return accountStatus, mailStatus


def cmd_zmprov_ma(id, key, val):
    """Executes shell command 'zmprov ma ...' """
    cmd = sh.Command(ZMPROV)
    try:
        cmd('ma', id, key, val)
        return True
    except sh.ErrorReturnCode:
        return False


def cmd_zmprov_ga(id, key):
    """Executes shell command 'zmprov ga ...' """
    cmd = sh.Command(ZMPROV)
    try:
        return cmd('ga', id, key).out
    except sh.ErrorReturnCode, e:
        return str(e)
