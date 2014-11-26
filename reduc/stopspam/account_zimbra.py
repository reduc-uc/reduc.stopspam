import sh

from reduc.stopspam.account import IAccount


class ZimbraAccount(IAccount):
    """Handles Zimbra account status."""

    def __init__(self, zmprov_path):
        self.zmprov = sh.Command(zmprov_path)

    def status(self, id):
        """Returns the status of the given user. """
        accountStatus = self._zmprov_ga(id, 'zimbraAccountStatus').split()[-1]
        mailStatus = self._zmprov_ga(id, 'zimbraMailStatus').split()[-1]
        return accountStatus, mailStatus

    def suspend(self, id):
        """ Suspends the given user."""
        self._zmprov_ma(id, 'zimbraAccountStatus', 'locked')
        self._zmprov_ma(id, 'zimbraMailStatus', 'disabled')
        return True

    def reactivate(self, id):
        """Reactivates the give user."""
        self._zmprov_ma(id, 'zimbraAccountStatus', 'active')
        self._zmprov_ma(id, 'zimbraMailStatus', 'enabled')
        return True

    def _zmprov_ma(self, id, key, val):
        """Executes shell command 'zmprov ma ...' """
        try:
            self.zmprov('ma', id, key, val)
            return True
        except sh.ErrorReturnCode:
            return False

    def _zmprov_ga(self, id, key):
        """Executes shell command 'zmprov ga ...' """
        try:
            return self.zmprov('ga', id, key).stdout
        except sh.ErrorReturnCode, e:
            return str(e)
