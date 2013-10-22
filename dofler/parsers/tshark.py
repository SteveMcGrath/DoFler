from base import BaseParser, log
import time

config = {
    'command': 'tshark -i {IF}',
    'prefix': 'tshark'
}

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

    def parse(self, line):
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