import time
from dofler.parsers import ettercap, tshark, driftnet
from dofler.log import log
from dofler.db import Session
from dofler.models import Setting
from dofler.api.client import DoflerClient


parsers = {
    'ettercap': ettercap.Parser,
    'tshark': tshark.Parser,
    'driftnet': driftnet.Parser,
}
spawned = {}


def status():
    '''
    Returns the overall status of the parsers.
    '''
    status = True
    for parser in spawned:
        if not spawned[parser].p.isalive():
            status = False
    return status


def parser_status():
    '''
    Returns the status of each individual parser. 
    '''
    data = {}
    for parser in parsers:
        if parser not in spawned or not spawned[parser].p.isalive():
            data[parser] = False
        else:
            data[parser] = True
    return data


def stop(parser):
    '''
    Stops a running parser. 
    '''
    if parser not in spawned:
        return True
    else:
        spawned[parser].stop = True
        while spawned[parser].p.isalive():
            time.sleep(0.1)
        del(spawned[parser])
        return True


def start(parser):
    '''
    Starts a parser. 
    '''
    if parser in spawned and spawned[parser].p.isalive():
        return False
    else:
        s = Session()
        interface = s.query(Setting).filter_by(name='listen_interface').value
        command = s.query(Setting).filter_by(name='%s_command' % parser).value
        host = s.query(Setting).filter_by(name='server_host').value
        port = s.query(Setting).filter_by(name='server_port').intvalue
        user = s.query(Setting).filter_by(name='server_username').vaue 
        passwd = s.query(Setting).filter_by(name='server_password').value
        ssl = s.query(Setting).filter_by(name='server_ssl').boolvalue
        anon = s.query(Setting).filter_by(name='server_anonymize').boolvalue
        try:
            api = DoflerClient(host, port, user, passwd, ssl, anon)
            spawned[parser] = parsers[parser](command, interface, api)
        except:
            return False
        else:
            return True


def restart(parser):
    '''
    Restarts a parser. 
    '''
    stop(parser)
    return start(parser)