import time

import sh
from commandr import command

from reduc.stopspam import log
from reduc.stopspam.zimbra import suspend


SLEEP_TIME = 300


@command
def serve():
    "Server to detect and suspend accounts that send spam."
    detectors = _get_detectors()
    while True:
        cases = [x for detector in detectors
                 for x in detector()]

        for id, msg in cases:
            # suspend(id)
            # mail_notify(id, msg)
            log.info('{0}: {1}'.format(id, msg))

        time.sleep(SLEEP_TIME)


def _get_detectors():
    """Returns a list of spam detectors."""
    return []
