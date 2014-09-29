from io import StringIO
from ConfigParser import ConfigParser


DEFAULT_CONFIG = u"""
[shell]
postqueue: /usr/local/bin/postqueue
rmqueue: /usr/local/bin/rmqueue
zmprov: '/opt/zimbra/bin/zmprov'

[zimbra]
server: noserver.nodomain

[smtp]
maillog: /var/log/mail.log
"""

config = ConfigParser()
config.readfp(StringIO(DEFAULT_CONFIG))
config.read('/etc/stopspam.cfg')


log = None
