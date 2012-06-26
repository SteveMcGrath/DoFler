from base import BaseParser
from BeautifulSoup import BeautifulSoup as soup
#from dofler.api.client import account
import cgi

class Parser(BaseParser):
    packet = ''
    builder = True
    cmd = 'tshark -T pdml -i {INTERFACE} -R\'http.request.method == "POST"\''

    def parse(self, line):
        # First thing we need to do is check to see if we are running
        # within an XML definition.  If so, then we need to turn the
        # builder on.
        if '<packet>' in line:
            self.builder = True

        # Now we need to start building the XML definition if the builder
        # is turned on.
        if self.builder:
            self.packet += line

        # Now we need to check to see if the parser is done building the
        # the definition.  If so, then set the builder to false so that we don't
        # get a ton of garbage.
        if '</packet>' in line:
            self.builder = False 
            self.parse_packet()
            self.packet = ''


    def parse_packet(self):
        packet = soup(self.packet)
        username = None
        password = None
        host = None
        try:
            host = packet.find('field', attrs={'name': 'http.host'}).get('show')
            print packet.find('proto', attrs={'name': 'data-text-lines'})
            post = packet.find('proto', attrs={'name': 'data-text-lines'})\
                         .findNext('field').get('show')
            data = cgi.parse_qsl(post)
        except AttributeError:
            data = ()

        for item in data:
            if len(item) == 2:
                opt, val = item

                for sel in ['log', 'nick' ,'user', 'username', 'uid', 'email']:
                    if sel in opt.lower() and username == None:
                        username = val

                for sel in ['pass', 'pw', 'word']:
                    if sel in opt.lower() and password == None:
                        password = val

        if username is not None and password is not None:
            print username, password, host, 'tshark-http'
            #account(username, password, host, parser='tshark-http')