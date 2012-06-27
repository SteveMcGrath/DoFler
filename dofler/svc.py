from dofler import monitor
import dofler.api.client
import dofler.api.server
import os
from dofler.config import config

def client():
    dofler.api.client.login()

    if config.getboolean('Ettercap', 'run'):
        print 'Starting Ettercap Monitor...'
        ettercap = monitor.ettercap.Parser()
        ettercap.start()

    if config.getboolean('TShark-http', 'run'):
        print 'Starting TShark-http monitor'
        tshark = monitor.tshark.Parser()
        tshark.start()

    if config.getboolean('Driftnet', 'run'):
        print 'Starting Driftnet monitor...'
        tcpxtract = monitor.driftnet.Parser()
        tcpxtract.start()

    print 'Running.'


def server():
    if not os.path.exists('/var/cache/dofler'):
        os.mkdir('/var/cache/dofler')
    dofler.api.server.serve()