import time
import smtplib
import logging

from commandr import command

from reduc.stopspam import config
from reduc.stopspam.detectors import get_detectors
from reduc.stopspam.command_queue import rmqueue
from reduc.stopspam.command_account import account_suspend


@command
def serve():
    "Server to detect and suspend accounts that send spam."
    logging.info('Starting stopspam daemon')
    sleep_time = config.getint('server', 'sleep_time')
    exceptions = config.get('server', 'exceptions', '').split()
    domain = config.get('server', 'domain', '')

    detectors = [detector for detector in get_detectors(config)]
    notify = MailNotify(config)

    while True:
        for detector in detectors:
            try:
                id, reason = '', ''
                cases = detector.execute()

                for id, reason in cases:
                    if id in exceptions:
                        continue

                    if domain not in id:
                        continue

                    logging.info('suspending {0}: {1}'.format(id, reason))
                    rmqueue(id)
                    account_suspend(id)
                    notify.execute(id, reason)

            except Exception, e:
                logging.error('{0}: {1} - {2}'.format(detector, id, reason))
                logging.exception(e)

        time.sleep(sleep_time)


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

        self.smtp.connect(self.mail_server)
        for dest in self.mail_to:
            mail = self.mail_message.format(id, reason)
            self.smtp.sendmail(self.mail_from, dest, mail)
        self.smtp.quit()
