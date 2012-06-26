from dofler import monitor
from dofler.config import config

def start():
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

    if config.getboolean('Driftnet', 'run'):
        print 'Starting Driftnet monitor...'
        driftnet = monitor.driftnet.Parser()
        driftnet.run(config.get('Driftnet', 'interface'),
                     conifg.getint('Driftnet', 'timer'),
                     config.getboolean('Driftnet', 'promisc'))

    print 'Running.'