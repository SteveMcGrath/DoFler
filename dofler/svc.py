from dofler import monitor
import dofler.api.client
from dofler.config import config

def start():
    dofler.api.client.login()

    if config.getboolean('Ettercap', 'run'):
        print 'Starting Ettercap Monitor...'
        ettercap = monitor.ettercap.Parser()
        ettercap.run(config.get('Ettercap', 'interface'),
                     conifg.getint('Ettercap', 'timer'),
                     config.getboolean('Ettercap', 'promisc'))

    if config.getboolean('TShark-http', 'run'):
        print 'Starting TShark-http monitor'
        tshark = monitor.tshark.Parser()
        tshark.run(config.get('TShark-http', 'interface'),
                   conifg.getint('TShark-http', 'timer'),
                   config.getboolean('TShark-http', 'promisc'))

    if config.getboolean('TCPXtract', 'run'):
        print 'Starting Driftnet monitor...'
        tcpxtract = monitor.tcpxtract.Parser()
        tcpxtract.run(config.get('TCPXtract', 'interface'),
                      conifg.getint('TCPXtract', 'timer'),
                      config.getboolean('TCPXtract', 'promisc'))

    print 'Running.'