import time
from dofler.parsers import ettercap, tshark, driftnet
from dofler.db import Session
from dofler.common import setting, log
from dofler.api.client import DoflerClient


parsers = {
    'ettercap': ettercap.Parser,
    'tshark': tshark.Parser,
    'driftnet': driftnet.Parser,
}
spawned = {}


def autostart(delay_start=0):
    '''
    Automatically starts up the parsers that are enabled if autostart is
    turned on. 
    '''
    s = Session()
    if setting('autostart').boolvalue:
        if setting('driftnet_enabled').boolvalue:
            start('driftnet', delay_start)
        if setting('ettercap_enabled').boolvalue:
            start('ettercap', delay_start)
        if setting('tshark_enabled').boolvalue:
            start('tshark', delay_start)


def status():
    '''
    Returns the overall status of the parsers.
    '''
    status = True
    for parser in spawned:
        if not spawned[parser].is_alive():
            status = False
    return status


def parser_status():
    '''
    Returns the status of each individual parser. 
    '''
    data = {}
    for parser in parsers:
        if parser not in spawned or not spawned[parser].is_alive():
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
        spawned[parser].terminate()
        while spawned[parser].is_alive():
            time.sleep(0.1)
        #spawned[parser].cleanup()
        del(spawned[parser])
        return True


def start(parser, delay_start=0):
    '''
    Starts a parser. 
    '''
    if parser in spawned and spawned[parser].is_alive():
        return False
    else:
        try:
            spawned[parser] = parsers[parser]()
            spawned[parser].delay = delay_start
            spawned[parser].start()
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