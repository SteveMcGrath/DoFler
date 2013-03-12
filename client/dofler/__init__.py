import api
import config
import log
import monitor

def start():
    api.login()
    pids = []
    c = config.config
    parsers = monitor.get_parsers()
    for parser in parsers:
        stanza = 'Parser: %s' % parser
        if stanza in c.sections() and c.getboolean(stanza, 'enabled'):
            pid = parsers[parser]()
            pid.start()
            pids.append(pid)

