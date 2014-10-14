import time
import smtplib
import logging

from commandr import command

from reduc.stopspam import config
from reduc.stopspam.zimbra import suspend
from reduc.stopspam.detectors import get_detectors


SLEEP_TIME = config.getint('server', 'sleep_time')
EXCEPTIONS = config.get('server', 'exceptions', '').split()
ENABLE_SUSPEND = config.getboolean('server', 'enable_suspend')

ENABLE_NOTIFY = config.getboolean('notify', 'enable_notify')
MAIL_SERVER = config.get('notify', 'mail_server')
MAIL_FROM = config.get('notify', 'mail_from')
MAIL_TO = config.get('notify', 'mail_to', '').split()
MAIL_MESSAGE = config.get('notify', 'message', 'Spam from {0}: {1}.')


@command
def serve():
    "Server to detect and suspend accounts that send spam."
    logging.info('Starting stopspam daemon')
    commands = [command for command in get_detectors(config)]

    while True:
        cases = []
        for command in commands:
            try:
                cases += [(id, reason) for (id, reason) in command.execute()
                          if id not in EXCEPTIONS]
            except Exception, e:
                logging.error(str(e))

        for id, reason in cases:
            logging.info('{0}: {1}'.format(id, reason))

            if ENABLE_SUSPEND:
                try:
                    suspend(id)
                    logging.info('{0} suspended'.format(id))
                except Exception, e:
                    logging.exception(e)

            if ENABLE_NOTIFY:
                _send_mail(MAIL_TO, id, reason)

        time.sleep(SLEEP_TIME)


def _send_mail(dests, id, reason):
    """Sends a mail to admin notifying the suspension of user 'id'."""
    smtp = smtplib.SMTP(MAIL_SERVER)
    for dest in dests:
        mail = MAIL_MESSAGE.format(dest, reason)
        smtp.sendmail(MAIL_FROM, dest, mail)
