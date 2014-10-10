from collections import defaultdict

import sh
from commandr import command

from reduc.stopspam import config


POSTQUEUE = config.get('shell', 'postqueue')
RMQUEUE = config.get('shell', 'rmqueue')
N_ENTRIES = 10


class QueueEntry:
    def __init__(self, id, size, date, sender, info, receivers):
        self.id = id
        self.size = size
        self.date = date
        self.sender = sender
        self.info = info
        self.receivers = receivers

    @staticmethod
    def from_lines(lines):
        """Converts a list of lines in a QueueEntry"""
        header = lines.pop(0)
        info = lines.pop(0)
        receivers = [x.strip() for x in lines]
        parts = header.split()
        sender = parts.pop()
        id = parts.pop(0)
        size = parts.pop(0)
        date = ' '.join(parts)
        return QueueEntry(id, size, date, sender, info, receivers)

    @staticmethod
    def queue_from_lines(lines):
        """Converts a list of lines in a list of QueueEntry."""
        # Remove header line, if present
        if lines and lines[0][0] == '-':
            lines = lines[1:]

        record_lines = []
        queue = []

        for line in lines:
            if not line:
                queue.append(QueueEntry.from_lines(record_lines))
                record_lines = []
                continue
            record_lines.append(line)

        return queue

    def __repr__(self):
        return "QueueEntry({0}, {1}, '{2}', {3}, '{4}', {5})".format(
            self.id, self.size, self.date,
            self.sender, self.info, self.receivers)

    def __str__(self):
        return '{0} {1} {2} {3} {4} {5}'.format(
            self.id, self.size, self.date, self.sender,
            self.receivers, self.info)


@command(category='queue')
def postqueue():
    """Gets postfix queue info"""
    queue = get_postqueue()
    for entry in queue:
        print entry


def get_postqueue():
    """Wrapper for potsqueue that return objects instead of text"""
    lines = cmd_postqueue_p()
    queue = QueueEntry.queue_from_lines(lines)
    return queue


@command('queue-by-senders', category='queue')
def queue_by_senders(n=N_ENTRIES):
    """List of senders with more entries in the queue"""
    for sender, entries in get_queue_by_senders(n):
        print len(entries), sender


def get_queue_by_senders(n):
    """Returns a list of n (sender, [QueueEntry]) sorted by # of entries."""
    queue = get_postqueue()
    lst_queue = dict_from_queue(queue).items()
    lst_queue.sort(reverse=True, cmp=cmp_by_entries)
    return lst_queue[:n]


@command('queue-by-messages', category='queue')
def queue_by_messages(n=N_ENTRIES):
    """List of senders with more messages to be send"""
    for sender, entries in get_queue_by_messages(n):
        print num_of_messages(entries), sender


def get_queue_by_messages(n=N_ENTRIES):
    """Returns a list of n (sender, [QueueEntry]) sorted by # of messages."""
    queue = get_postqueue()
    lst_queue = dict_from_queue(queue).items()
    lst_queue.sort(reverse=True, cmp=cmp_by_messages)
    return lst_queue[:n]


def cmp_by_entries(a, b):
    """Compares pairs of (sender, [QueueEntry]) by the number of entries."""
    return cmp(len(a[1]), len(b[1]))


def cmp_by_messages(a, b):
    """Compares pairs of (sender, [QueueEntry]) by the number of messages."""
    return cmp(num_of_messages(a[1]), num_of_messages(b[1]))


def num_of_messages(lst):
    """Returns the number of messages in a list of QueueEntry."""
    return sum([len(x.receivers) for x in lst])


def dict_from_queue(queue):
    """Returns a dict from queue qith sender as key."""
    dct = defaultdict(list)
    for entry in queue:
        dct[entry.sender].append(entry)
    return dct


def cmd_postqueue_p():
    """Executes shell command 'postqueue -p'"""
    command = sh.Command(POSTQUEUE)
    try:
        lines = command('-p').stdout.splitlines()
        return lines
    except sh.ErrorReturnCode, e:
        return str(e)


@command(category='queue')
def rmqueue(mails=[]):
    """Remove the messages queued for the given users.

    The users can be given as a list of mails or a list of comma separated
    mails."""
    mails = [y for x in [x.split(',') for x in mails]
             for y in x]
    for mail in mails:
        print "Deleting messages from '{0}'...".format(mail)
        print cmd_rmqueue(mail)


def cmd_rmqueue(mail):
    """Executes shell command for 'rmqueue'."""
    cmd = sh.Command(RMQUEUE)
    try:
        out = cmd(mail)
        return out.stdout
    except sh.ErrorReturnCode, e:
        return '    ' + str(e).splitlines()[-1]
