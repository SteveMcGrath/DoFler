import tshark
import time
import json
from dofler.log import log
import dofler.api
from BeautifulSoup import BeautifulSoup as soup

class Parser(tshark.Parser):
    '''This parser is designed the get statistical information about all of the
    traffic we see on the interface.  It will then report that information back
    up to the API once every 60 seconds.
    '''
    stanza = 'tshark-stats' # The configuration stanza.
    protos = {}             # The protocol dictionary.
    wait_timer = 0          # This is the timer we will be using to check when
                            # to upload to the API and flush out the protos
                            # dictionary.
    interval = 60           # Number of seconds to wait to push to API.
    cmd = 'tshark -T psml -i {INTERFACE} {PROMISC} -S -b filesize:1000 -b files:3 -w /tmp/tshark-stats.pcap'
    # Example PSML Packet for reference.
    # <packet>
    # <section>216027</section>
    # <section>372.025677</section>
    # <section>10.10.100.82</section>
    # <section>77.85.14.100</section>
    # <section>UDP</section>
    # <section>Source port: 1024  Destination port: 57057</section>
    # </packet>

    def parse_packet(self):
        '''This function will parse the needed data from the packet XML
        definition and send the data to the API.
        '''
        packet = soup(self.packet)  # The BeautifulSoup parser object of the XML
        proto = packet.findAll('section')[-2].text
        if proto not in self.protos:
            self.protos[proto] = 0
        self.protos[proto] += 1
        if (int(time.time()) - self.wait_timer) >= self.interval:
            for proto in self.protos:
                log.debug('%s Stats: %s: %s' % (self.stanza, proto, self.protos[proto]))
                dofler.api.stat(proto, self.protos[proto])
            self.wait_timer = int(time.time())
            self.protos = {}



