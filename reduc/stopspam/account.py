class IAccount:
    """Interface for handling user accounts."""

    def status(self, id):
        """ Returns the status of the given user."""
        raise NotImplemented

    def suspend(self, id):
        """ Suspends the given user. """

    def reactivate(self, id):
        """ Reactivates the give user. """
