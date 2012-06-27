from dofler import monitor
import dofler.api.client
import dofler.api.server
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

    if config.getboolean('TCPXtract', 'run'):
        print 'Starting Driftnet monitor...'
        tcpxtract = monitor.tcpxtract.Parser()
        tcpxtract.start()

    print 'Running.'


def server():
    dofler.api.server.serve()