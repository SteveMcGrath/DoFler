import dofler.monitor
import dofler.api.client
import dofler.api.server
import os
from dofler.config import config

def client():
    dofler.api.client.login()
    for parser in dofler.monitor.get_parsers():
        parser.start()

def server():
    if not os.path.exists('/var/cache/dofler'):
        os.mkdir('/var/cache/dofler')
    dofler.api.server.serve()