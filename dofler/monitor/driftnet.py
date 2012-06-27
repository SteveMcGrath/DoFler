from base import BaseParser
import re
import os
import dofler.api.client

class Parser(BaseParser):
    #rimage = re.compile(r'exporting to (.*?)[\r]{0,1}$')
    cmd = 'driftnet -ai {INTERFACE} -d /tmp'
    stanza = 'Driftnet'

    def parse(self, line):
        filename = line.strip('\r\n')
        dofler.api.client.image(filename)
        os.remove(filename)