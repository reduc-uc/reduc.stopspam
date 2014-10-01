from io import StringIO
import logging
import logging.config
from ConfigParser import ConfigParser, NoSectionError


CONFIG_FILE = '/etc/stopspam'
DEFAULT_CONFIG = u"""
[shell]
postqueue: /usr/local/bin/postqueue
rmqueue: /usr/local/bin/rmqueue
zmprov: /opt/zimbra/bin/zmprov

[zimbra]
server: noserver.nodomain

[smtp]
maillog: /var/log/mail.log

[notify]
enable_notify: false
mail_server: smtp.blah.com
mail_from: stopspam@blah.com
mail_to: a@blah.com b@blah.com
message: stopspam has detected an irregular activity with the account
    {0}: {1}

[server]
detectors:
exceptions:
notify_list:
sleep_time: 300

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
