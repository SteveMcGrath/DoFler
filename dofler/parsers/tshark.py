from base import BaseParser, log
from BeautifulSoup import BeautifulSoup as soup
import time

class Parser(BaseParser):
    '''
    tshark parser.  This parser will be looking at the basic output of tshark
    and count all of the packets & protocols that it is seeing.  It will then
    report back every minute the protocols and the counts for each associated
    with them.
    '''
    name = 'tshark'
    protos = {}
    counter = 0
    builder = False
    packet = ''

    def parse(self, line):
        '''
        tshark base parser 
        '''
        # For simplicities sake, we will be defaulting to the PSML parser.  In
        # the future there may be a need to run the line parser, however for now
        # you will have to specifically override that here.
        self.parse_psml(line)


    def parse_base(self, line):
        '''
        tshark line parser
        '''
        data = line.split()
        if len(data) >= 5:
            proto = data[4]

            # If we dont see the protocol yet in the protos dictionary, we need
            # to initialize it.  After that, we can then increment regardless.
            if proto not in self.protos:
                self.protos[proto] = 0
            self.protos[proto] += 1

            # If the counter timer is set to 0, then this is the first packet
            # we have parsed.  Set the counter to the current time so that we
            # dont send a single packet stat to the API.
            if self.counter == 0:
                self.counter = int(time.time())

            # Once we reach 60 seconds, we need to purge out the protocol counts
            # that we have counted.  Make an API call for each proto we have,
            # then reset the counter timer and the protos dictionary.
            if (int(time.time()) - self.counter) >= 60:
                for proto in self.protos:
                    log.debug('TSHARK: sending %s=%s' % (proto, self.protos[proto]))
                    self.api.stat(proto, self.protos[proto])
                self.counter = int(time.time())
                self.protos = {}


    def parse_psml(self, line):
        '''
        tshark psml parser 
        '''
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
        '''
        This function will parse the needed data from the packet PSML XML
        definition and send the data to the API.
        '''
        # If the counter timer is set to 0, then this is the first packet
        # we have parsed.  Set the counter to the current time so that we
        # dont send a single packet stat to the API.
        if self.counter == 0:
            self.counter = int(time.time())

        # Next we instantiate a BeautifulSoup object to parse the packet and
        # pull out the protocol name.
        packet = soup(self.packet)
        proto = packet.findAll('section')[4].text


        # If we dont see the protocol yet in the protos dictionary, we need
        # to initialize it.  After that, we can then increment regardless.
        if proto not in self.protos:
            self.protos[proto] = 0
        self.protos[proto] += 1

        # Once we reach 60 seconds, we need to purge out the protocol counts
        # that we have counted.  Make an API call for each proto we have,
        # then reset the counter timer and the protos dictionary.
        if (int(time.time()) - self.counter) >= 60:
            for proto in self.protos:
                log.debug('TSHARK: sending %s=%s' % (proto, self.protos[proto]))
                self.api.stat(proto, self.protos[proto])
            self.counter = int(time.time())
            self.protos = {}