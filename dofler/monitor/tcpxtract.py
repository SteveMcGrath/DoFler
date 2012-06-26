from base import BaseParser
import re
import os
import dofler.api.client

class Parser(BaseParser):
	rimage = re.compile(r'exporting to (.*?)$')
    cmd = 'tcpxtract -d {INTERFACE} -o /tmp'

    def parse(self, line):
        files = self.rimage.findall(line):
        if len(files) > 0:
            filename = files[0]
            dofler.api.client.image(filename)
            os.remove(filename)