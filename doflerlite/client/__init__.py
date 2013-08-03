import api
import config
import log
import monitor

def start():
    pids = []
    c = config.config
    parsers = monitor.get_parsers()
    for parser in parsers:
        stanza = 'Parser: %s' % parser
        if stanza in c.sections() and c.getboolean(stanza, 'enabled'):
            log.log.debug('Starting up %s parser' % parser)
            pid = parsers[parser]()
            pid.start()
            pids.append(pid)
    log.log.debug('PIDS: %s' % pids)

