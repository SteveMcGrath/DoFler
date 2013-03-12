from base import BaseParser
import re
import os
import dofler.api

class Parser(BaseParser):
    rimage = re.compile(r'exporting to (.*?)[\r]{0,1}$')
    cmd = 'tcpxtract -d {INTERFACE} -o /tmp'
    stanza = 'tcpxtract'

    def parse(self, line):
        files = self.rimage.findall(line)
        if len(files) > 0:
            filename = files[0]
            dofler.api.image(filename.strip('\r'))
            os.remove(filename)