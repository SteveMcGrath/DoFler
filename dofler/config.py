from ConfigParser import ConfigParser
import os

config = ConfigParser()
if os.path.exists('/etc/doflerdb.conf'):
    config.read('/etc/doflerdb.conf')
else:
    config.add_section('Database')
    config.set('Database', 'db', 'sqlite:////var/lib/dofler.db')
    with open('/etc/doflerdb.conf', 'w') as cfile:
        config.write(cfile)

