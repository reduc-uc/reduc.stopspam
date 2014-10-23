import logging

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

    def suspend(self, id):
        pass
