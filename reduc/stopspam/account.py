class IAccount:
    """Interface for handling user accounts."""

    def status(self, id):
        """ Returns the status of the given user."""
        raise NotImplemented

    def suspend(self, id):
        """ Suspends the given user.
        Returns True if the user was suspended, False if doesn't exists
        and error in other case."""
        raise NotImplemented

    def reactivate(self, id):
        """ Reactivates the give user.
        Returns True if the user was reactivated, False if doen't exists
        and error in other case"""
        raise NotImplemented
