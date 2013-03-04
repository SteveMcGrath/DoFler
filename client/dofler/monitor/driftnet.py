from base import BaseParser
from dofler.log import log
import re
import os
import dofler.api

class Parser(BaseParser):
    #rimage = re.compile(r'exporting to (.*?)[\r]{0,1}$')
    cmd = 'driftnet -ai {INTERFACE} -d /tmp'
    stanza = 'Driftnet'

    def parse(self, line):
        filename = line.strip('\r\n')
        log.debug('%s sending image: %s' % (self.stanza, filename))
        dofler.api.image(filename)
        os.remove(filename)