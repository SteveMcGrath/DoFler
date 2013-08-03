import logging
from doflerlite.client.config import config

_loglevels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

log = logging.getLogger('DoFler')

# This is the console output handler
if config.getboolean('Logging', 'console'):
    stderr = logging.StreamHandler()
    console_format = logging.Formatter('%(levelname)s %(message)s')
    stderr.setFormatter(console_format)
    log.setLevel(_loglevels[config.get('Logging', 'level')])
    log.addHandler(stderr)

# This is the file handler, and is optional.
if config.getboolean('Logging', 'logfile'):
    hdlr = logging.FileHandler(config.get('Logging', 'log_filename'))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    hdlr.setFormatter(formatter)
    log.setLevel(_loglevels[config.get('Logging', 'level')])
    log.addHandler(hdlr)