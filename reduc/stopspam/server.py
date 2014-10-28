import time
import smtplib
import logging

from commandr import command

from reduc.stopspam import config
from reduc.stopspam.suspend import get_suspend
from reduc.stopspam.detectors import get_detectors


SLEEP_TIME = config.getint('server', 'sleep_time')
EXCEPTIONS = config.get('server', 'exceptions', '').split()
ENABLE_SUSPEND = config.getboolean('server', 'enable_suspend')


@command
def serve():
    "Server to detect and suspend accounts that send spam."
    logging.info('Starting stopspam daemon')
    detectors = [detector for detector in get_detectors(config)]
    suspend = get_suspend(config)
    notify = MailNotify(config)

    while True:
        cases = []
        for detector in detectors:
            try:
                cases += [(id, reason) for (id, reason) in detector.execute()
                          if id not in EXCEPTIONS]
            except Exception, e:
                logging.error(str(e))

        for id, reason in cases:
            logging.info('{0}: {1}'.format(id, reason))
            suspend.execute(id)
            notify.execute(id, reason)

        time.sleep(SLEEP_TIME)


class MailNotify:
    """Mail notification Command."""
    def __init__(self, config):
        self.enable_notify = config.getboolean('notify', 'enable_notify')
        self.mail_server = config.get('notify', 'mail_server')
        self.mail_from = config.get('notify', 'mail_from')
        self.mail_to = config.get('notify', 'mail_to', '').split()
        self.mail_message = config.get('notify',
                                       'message', 'Spam from {0}: {1}.')
        self.smtp = smtplib.SMTP(self.mail_server)

    def execute(self, id, reason=''):
        if not self.enable_notify:
            return

        for dest in self.mail_to:
            mail = self.mail_message.format(id, reason)
            self.smtp.sendmail(self.mail_from, dest, mail)
