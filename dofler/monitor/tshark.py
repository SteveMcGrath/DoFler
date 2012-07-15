from base import BaseParser
from BeautifulSoup import BeautifulSoup as soup
from dofler.log import log
import dofler.api.client
import cgi

class Parser(BaseParser):
    packet = ''
    builder = True
    promisc = {True: '', False: '-p'}
    stanza = 'TShark-http'
    cmd = 'tshark -T pdml -i {INTERFACE} {PROMISC} -R\'http.request.method == "POST"\' -S'

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
        '''This function will parse the needed data from the packet XML
        definition and send the data to the API.
        '''
        packet = soup(self.packet)  # The BeautifulSoup parser object of the XML
        username = None             # Preload of username
        password = None             # Preload of password
        host = None                 # Preload of host

        # Here we are attempting to parse out the data from the packet XML
        # definition.  If we run into any problems, then just return an empty
        # data tuple so that the rest of the code runs through properly and
        # ignores the data.
        try:
            host = packet.find('field', attrs={'name': 'http.host'}).get('show')
            post = packet.find('proto', attrs={'name': 'data-text-lines'})\
                         .findNext('field').get('show')
            data = cgi.parse_qsl(post)
        except:
            data = ()

        # Here is where we will start trying to parse out the username and
        # password if we see them.  We will be using some simple "if x in y"
        # logic to allow us to check for subsets of data.
        for item in data:
            if len(item) == 2:
                opt, val = item

                # This is the username definitions.  As app developers use a
                # lot of different notations for a username, we have to check
                # for several of them.
                for sel in ['log', 'nick' ,'user', 'username', 'uid', 'email']:
                    if sel in opt.lower() and username == None:
                        username = val

                # And the password definitions.  As you can see, this is a lot
                # easier to parse ;)
                for sel in ['pass', 'pw', 'word']:
                    if sel in opt.lower() and password == None:
                        password = val

        # If we have all the data, then lets send it on to the API.
        if username is not None and password is not None and host is not None:
            log.debug('%s is sending Account <%s>' % (self.stanza, username))
            dofler.api.client.account(username, password, 
                                      host, 'HTTP', 'tshark-http')  