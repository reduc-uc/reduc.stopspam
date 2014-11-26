import re
from time import time
from datetime import datetime
from itertools import groupby
from collections import namedtuple

from reduc.stopspam.command_queue import get_queue_by_senders, \
    get_queue_by_messages

from reduc.stopspam.logfile import LogFile


def get_detectors(config):
    """Returns a list of spam detectors."""
    detector_string = config.get('server', 'detectors', '')
    detectors = [_detector_from_name(x, config)
                 for x in detector_string.split()]
    return detectors


def _detector_from_name(name, config):
    """Converts a string in a detector function."""
    # TODO: Convert fqdn in functions. By now, use globals()
    detector_class = globals()[name]
    return detector_class(config)


class QueueBySenders:
    """Command that returns list of ids that have more entries in queue than
    the threshold"""

    def __init__(self, config):
        self.threshold = config.getint('QueueBySenders', 'threshold')

    def execute(self):
        ids = [(x[0], '{0} entries in mail queue'.format(len(x[1])))
               for x in get_queue_by_senders(None)
               if len(x[1]) >= self.threshold]
        return ids


class QueueByMessages:
    """Command that returns list of ids that have more messages in queue than
    the threshold"""

    def __init__(self, config):
        self.threshold = config.getint('QueueByMessages', 'threshold')

    def execute(self):
        ids = [(x[0], '{0} messages in mail queue'.format(len(x[1])))
               for x in get_queue_by_messages(None)
               if len(x[1]) >= self.threshold]
        return ids


MailEntry = namedtuple('MailEntry', ['id', 'expire'])


class MaillogDetector:
    """Base class for maillog related detectors."""
    MESSAGE = '{0} messages in maillog'

    def __init__(self, config):
        maillog = config.get('files', 'maillog')
        self.logfile = LogFile(maillog)
        self.logfile.seek_end()
        self.entries = []
        self.update_entries()

    def execute(self):
        self._purge_old_entries()
        self.update_entries()
        ids = [(x[0], self.MESSAGE.format(x[1]))
               for x in self.detected_from_entries()
               if x[0] and x[1] >= self.threshold]
        return ids

    def update_entries(self, new_entries=None):
        if new_entries is None:
            new_entries = self._get_new_entries()

        self.entries += new_entries

    def detected_from_entries(self):
        """Returs a list of (id, num_of_entries) of the users whose entries
        in maillog surpase the threshold."""
        entrygroup = [list(e) for k, e in groupby(sorted(self.entries),
                                                  lambda x: x.id)]
        result = [(x[0].id, len(x)) for x in entrygroup
                  if len(x) >= self.threshold]
        return result

    def _get_new_entries(self):
        """Return list of new entries read from logfile."""
        lines = self.logfile.read().splitlines()
        new_entries = [self._entry_from_line(line)
                       for line in lines
                       if self._filter_line(line)]
        return new_entries

    def _entry_from_line(self, line):
        """Converts a logfile line in an entry."""
        raise NotImplemented()

    def _filter_line(self, line):
        """True if this logfile line is relevant for this detector."""
        raise NotImplemented()

    def _purge_old_entries(self, now=None):
        """Purge entries older than the TTL"""
        if now is None:
            now = time()
        self.entries = [x for x in self.entries if x.expire > now]

    def time_from_syslog(str):
        # TODO: finish this method. Syslog doesn't give the year
        dt = datetime.strptime(str, "%b %d %H:%M:%S")
        return dt


class MaillogByQmgr(MaillogDetector):
    """Command that returns list of ids that have more messages in maillog
    than the threshold"""
    MESSAGE = '{0} messages in maillog'
    mail_re = re.compile('<(.*)>')

    def __init__(self, config):
        MaillogDetector.__init__(self, config)
        self.threshold = config.getint('MaillogByQmgr', 'threshold')
        self.ttl = config.getint('MaillogByQmgr', 'ttl')

    def _entry_from_line(self, line):
        """Converts a logfile line in an entry."""
        part = line.split()
        mail = self.mail_re.search(part[6]).groups()[0]
        # We're cheating here. Instead of parsing the (#$%# incomplete)
        # date given by syslog, we'll pretend all they happened early.
        # This means that TTL should be bigger than sleep_time
        expire = time() + self.ttl
        entry = MailEntry(mail, expire)
        return entry

    def _filter_line(self, line):
        """True if this logfile line is relevant for this detector."""
        return 'postfix/qmgr' in line and 'from' in line


class MaillogBySasl(MaillogDetector):
    """Command that returns list of ids that have more messages in maillog
    than the threshold"""
    MESSAGE = '{0} sasl connections in maillog'

    def __init__(self, config):
        MaillogDetector.__init__(self, config)
        self.threshold = config.getint('MaillogBySasl', 'threshold')
        self.ttl = config.getint('MaillogBySasl', 'ttl')
        try:
            self.domain = config.get('MaillogBySasl', 'domain')
        except:
            self.domain = config.get('server', 'domain', '')

    def _entry_from_line(self, line):
        """Converts a logfile line in an entry."""
        part = line.split()
        uid = part[8].split('=')[1]
        mail = '{0}@{1}'.format(uid, self.domain)
        # We're cheating here. Instead of parsing the (#$%# incomplete)
        # date given by syslog, we'll pretend all they happened early.
        # This means that TTL should be bigger than sleep_time
        expire = time() + self.ttl
        return MailEntry(mail, expire)

    def _filter_line(self, line):
        """True if this logfile line is relevant for this detector."""
        return 'sasl_user' in line and '@{0}'.format(self.domain) in line

