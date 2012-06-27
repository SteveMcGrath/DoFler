from base import BaseParser
import re
import os
import dofler.api.client

class Parser(BaseParser):
    rimage = re.compile(r'exporting to (.*?)[\r]{0,1}$')
    cmd = 'tcpxtract -d {INTERFACE} -o /tmp'
    stanza = 'TCPXtract'

    def parse(self, line):
        files = self.rimage.findall(line)
        if len(files) > 0:
            filename = files[0]
            dofler.api.client.image(filename.strip('\r'))
            #os.remove(filename)