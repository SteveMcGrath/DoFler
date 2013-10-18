import time
from dofler.parsers import ettercap, tshark, driftnet
from dofler.log import log
from dofler.db import Session
from dofler.common import setting
from dofler.api.client import DoflerClient


parsers = {
    'ettercap': ettercap.Parser,
    'tshark': tshark.Parser,
    'driftnet': driftnet.Parser,
}
spawned = {}


def autostart():
    '''
    Automatically starts up the parsers that are enabled if autostart is
    turned on. 
    '''
    s = Session()
    if setting('autostart', s).boolvalue:
        if setting('driftnet_enabled').boolvalue:
            start('driftnet')
        if setting('ettercap_enabled').boolvalue:
            start('ettercap')
        if setting('tshark_enabled').boolvalue:
            start('tshark')


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
        try:
            spawned[parser] = parsers[parser]()
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