import logging

log = logging.getLogger('stopspam')
handler = logging.FileHandler('/var/log/stopspam.log')
log.addHandler(handler)