from io import StringIO
import logging
import logging.config
from ConfigParser import ConfigParser, NoSectionError


CONFIG_FILE = '/etc/stopspam.cfg'
DEFAULT_CONFIG = u"""
[files]
postqueue: /usr/local/bin/postqueue
postsuper: /usr/local/bin/postsuper
zmprov: /opt/zimbra/bin/zmprov
maillog: /var/log/mail.log

[server]
account: Zimbra
detectors:
exceptions:
domain:
enable_suspend: true
sleep_time: 300

[notify]
enable_notify: false
mail_server: smtp.blah.com
mail_from: stopspam@blah.com
mail_to: a@blah.com b@blah.com
message: Subject: Stopspam: {0} {1}
  stopspam has detected an irregular activity with the account
  {0}: {1}

# -----------------
# Detectors
# -----------------

[QueueBySenders]
threshold: 45
ttl: 900

[QueueByMessages]
threshold: 45
ttl: 900

[MaillogByQmgr]
threshold: 45
ttl: 900

[MaillogBySasl]
threshold: 45
ttl: 900

# -----------------
# Log configuration
# -----------------

[loggers]
keys: root

[logger_root]
level: INFO
handlers: default

[formatters]
keys: default

[handlers]
keys: default

[handler_default]
class: FileHandler
level: INFO
formatter: default
args: ("/var/log/stopspam.log", )

[formatter_default]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
datefmt=

"""

config = ConfigParser()
config.readfp(StringIO(DEFAULT_CONFIG))
config.read(CONFIG_FILE)

logging.getLogger('stopspam')
logging.config.fileConfig(StringIO(DEFAULT_CONFIG))

try:
    logging.config.fileConfig(CONFIG_FILE)
except NoSectionError:
    # The idiotic logging module requires logging section in all its files
    pass
