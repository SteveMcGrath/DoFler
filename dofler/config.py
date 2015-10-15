from ConfigParser import ConfigParser
import os
import sys

if os.name == 'nt':
    DATA_PREFIX = os.path.dirname(sys.executable) + '\\share\\dofler\\'
else:
    DATA_PREFIX = "/".join(os.path.dirname(sys.executable).split("/")[:-1]) + '/share/dofler/'

if not os.path.exists('/var/lib/dofler'):
    os.makedirs('/var/lib/dofler')

config = ConfigParser()
if os.path.exists('/etc/dofler.conf'):
    config.read('/etc/dofler.conf')
else:
    config.add_section('Database')
    config.set('Database', 'db', 'sqlite:////var/lib/dofler/data.db')
    config.set('Database', 'setting_db', 'sqlite:////var/lib/dofler/settings.db')
    with open('/etc/dofler.conf', 'w') as cfile:
        config.write(cfile)

def update(setting):
    '''
    Updates the Configuration file with the in-memory config file.
    '''
    config.set('Database', 'db', setting)
    with open('/etc/dofler.conf', 'w') as cfile:
        config.write(cfile)