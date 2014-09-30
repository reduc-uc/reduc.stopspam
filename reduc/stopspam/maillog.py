import re
from collections import defaultdict

from commandr import command

from reduc.stopspam import config
from reduc.stopspam.logfile import LogFile


MAIL_LOG = config.get('smtp', 'maillog', '/var/log/mail.log')
N_ENTRIES = 10


@command('maillog-by-qmgr', category='maillog')
def maillog_by_qmgr(n=N_ENTRIES):
    """List of senders as indicated by qmgr."""
    mail_log = LogFile(MAIL_LOG)
    for sender, nconn in get_mail_log_by_qmgr(mail_log)[:n]:
        print '   ', nconn, sender


def get_mail_log_by_qmgr(mail_log, dct=None):
    """Returns list of senders with more entries in qmgr."""
    mail_re = re.compile('<(.*)>')

    def filter_qmgr(line):
        """Filters qmgr records."""
        if not 'postfix/qmgr' in line:
            return None
        try:
            part = line.split()
            mail = mail_re.search(part[6]).groups()[0]
            return mail or None
        except:
            return None

    return process_logfile(mail_log, filter_qmgr, dct)


@command('maillog-by-sasl', category='maillog')
def maillog_by_sasl(n=N_ENTRIES):
    """List of senders as indicated by sasl authentication."""
    mail_log = LogFile(MAIL_LOG)
    for sender, nconn in get_mail_log_by_sasl(mail_log)[:n]:
        print '   ', nconn, sender


def get_mail_log_by_sasl(mail_log, dct=None):
    """Returns list of senders with more entries with sasl auth."""

    def filter_sasl(line):
        """Filters sasl_user connections."""
        if not 'sasl_user' in line:
            return None
        try:
            part = line.split()
            mail = part[8].split('=')[1]
            return mail or None
        except:
            return None

    return process_logfile(mail_log, filter_sasl, dct)


def process_logfile(logfile, filter, dct=None):
    """Process a logfile, collecting the relevant info.

    filter takes a line and returns a userid if the line satifies
    certain critery."""
    if dct is None:
        dct = defaultdict(int)

    for line in logfile.read().splitlines():
        uid = filter(line)
        if uid is not None:
            dct[uid] += 1
    lst = dct.items()
    lst.sort(reverse=True, cmp=lambda x, y: cmp(x[1], y[1]))

    return lst
