import logging
import ldap
from  ldap import modlist

from reduc.stopspam.zimbra import suspend as zimbra_suspend


def get_suspend(config):
    """Returns an instance of the suspend command."""
    suspend_string = config.get('server', 'suspend', 'ZimbraSuspend')
    suspend_class = globals()[suspend_string]
    suspend = suspend_class(config)
    return suspend


class BaseSuspend:
    """Suspend command based on zimbra."""
    def __init__(self, config):
        self.enable_suspend = config.getboolean('server', 'enable_suspend')

    def execute(self, id):
        if not self.enable_suspend:
            return

        try:
            self.suspend(id)
            logging.info('{0} suspended'.format(id))
        except Exception, e:
            logging.exception(e)

    def suspend(self, id):
        raise NotImplemented


class ZimbraSuspend(BaseSuspend):
    """Suspend command based on zimbra."""
    def suspend(self, id):
        zimbra_suspend(id)


class LDAPSuspend(BaseSuspend):
    """Suspend command based on LDAP."""
    def __init__(self, config):
        BaseSuspend.__init__(self, config)
        self.uri = config.get('LDAP', 'uri')
        self.base_dn = config.get('LDAP', 'base_dn')
        self.root_dn = config.get('LDAP', 'root_dn')
        self.root_pwd = config.get('LDAP', 'root_pwd')
        self.filter = config.get('LDAP', 'filter')
        self.server = None

    def suspend(self, id):
        self._bind()
        dn, user = self._find(id)
        new_user = user.copy()
        new_user['zimbraAccountStatus'] = 'locked'
        new_user['zimbraMailStatus'] = 'disabled'
        ldif = modlist.modifyModlist(user, new_user)
        self.server.modify_s(dn, ldif)

    def _bind(self):
        self.server = ldap.ldapobject.ReconnectLDAPObject(self.uri)
        self.server.simple_bind(self.root_dn, self.root_pwd)

    def _find(self, id):
        msgid = self.server.search(self.base_dn,
                                   ldap.SCOPE_SUBTREE,
                                   self.filter.format(id))
        _type, data = self.server.result(msgid, all=0)
        dn, dct = data[0]
        print dn, dct
        return dn, dct
