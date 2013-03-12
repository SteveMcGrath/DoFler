import api
import config
import log
import monitor

def start():
    pids = []
    c = config.config
    parsers = monitor.get_parsers()
    for parser in parsers:
        stanza = 'Parser: ' % parser
        if stanza in c.sections() and c.getboolean(stanza, 'enabled'):
            pid = parsers[parser]()
            pid.start()
            pids.append(pid)

