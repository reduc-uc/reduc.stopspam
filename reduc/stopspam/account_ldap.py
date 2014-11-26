import ldap
from ldap import modlist

from reduc.stopspam.account import IAccount


class LDAPAccount(IAccount):
    """Handles user accounts via LDAP."""

    def __init__(self, uri, base_dn, root_dn, root_pwd, filter):
        self.uri = uri
        self.base_dn = base_dn
        self.root_dn = root_dn
        self.root_pwd = root_pwd
        self.filter = filter
        self.server = None

    def status(self, id):
        """ Returns the status of the given user."""
        self._bind()
        dn, user = self._find(id)
        if dn is None:
            return None
        accountStatus = self._first(user, 'zimbraAccountStatus', '???')
        mailStatus = self._first(user, 'zimbraMailStatus', '???')
        return accountStatus, mailStatus

    def suspend(self, id):
        """ Suspends the given user. """
        self._bind()
        dn, user = self._find(id)

        if dn is None:
            return False

        new_user = user.copy()
        new_user['zimbraAccountStatus'] = 'locked'
        new_user['zimbraMailStatus'] = 'disabled'
        ldif = modlist.modifyModlist(user, new_user)
        self.server.modify_s(dn, ldif)
        return True

    def reactivate(self, id):
        """ Reactivates the give user. """
        self._bind()
        dn, user = self._find(id)

        if dn is None:
            return False

        new_user = user.copy()
        new_user['zimbraAccountStatus'] = 'active'
        new_user['zimbraMailStatus'] = 'enabled'
        ldif = modlist.modifyModlist(user, new_user)
        self.server.modify_s(dn, ldif)
        return True

    def _bind(self):
        self.server = ldap.ldapobject.ReconnectLDAPObject(self.uri)
        self.server.simple_bind(self.root_dn, self.root_pwd)

    def _find(self, id):
        msgid = self.server.search(self.base_dn,
                                   ldap.SCOPE_SUBTREE,
                                   self.filter.format(id))
        _type, data = self.server.result(msgid, all=0)

        if not len(data):
            return None, None

        dn, dct = data[0]
        return dn, dct

    @staticmethod
    def _first(dct, key, default=None):
        """Returns the first value of a dictionary key."""
        val = dct.get(key, [default])
        return val[0]
