from commandr import command

from reduc.stopspam import config
from reduc.stopspam.account_ldap import LDAPAccount
from reduc.stopspam.account_zimbra import ZimbraAccount


@command('account-status', category='account')
def account_status(ids):
    """Prints status of accounts separated by comma."""
    account = _account_factory()
    ids = ids.split(',')
    print '# id, zimbraAccountStatus, zimbraMailStatus'
    for id in ids:
        stat = account.status(id)
        print '{0},{1},{2}'.format(id, stat[0], stat[1])


@command('account-suspend', category='account')
def account_suspend(ids):
    """Suspends accounts separates by comma."""
    account = _account_factory()
    ids = ids.split(',')
    for id in ids:
        account.suspend(id)


@command('account-reactivate', category='account')
def account_reactivate(ids):
    """Reactivates accounts separated by comma."""
    account = _account_factory()
    ids = ids.split(',')
    for id in ids:
        account.reactivate(id)


def _account_factory():
    """Returns the right handler for account."""
    account_type = config.get('server', 'account', 'Zimbra')
    if account_type == 'Zimbra':
        zmprov = config.get('Zimbra', 'zmprov')
        account = ZimbraAccount(zmprov)

    elif account_type == 'LDAP':
        uri = config.get('LDAP', 'uri')
        base_dn = config.get('LDAP', 'base_dn')
        root_dn = config.get('LDAP', 'root_dn')
        root_pwd = config.get('LDAP', 'root_pwd')
        filter = config.get('LDAP', 'filter')
        account = LDAPAccount(uri, base_dn, root_dn, root_pwd, filter)

    else:
        raise NotImplemented

    return account
