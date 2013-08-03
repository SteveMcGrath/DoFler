from base import BaseParser
from doflerlite.client.log import log
import re
import os
from doflerlite.client import api

class Parser(BaseParser):
    #rimage = re.compile(r'exporting to (.*?)[\r]{0,1}$')
    cmd = 'driftnet -ai {INTERFACE} -d /tmp'
    stanza = 'driftnet'

    def parse(self, line):
        filename = line.strip('\r\n')
        log.debug('%s sending image: %s' % (self.stanza, filename))
        api.image(filename)
        try:
        	os.remove(filename)
        except:
        	pass