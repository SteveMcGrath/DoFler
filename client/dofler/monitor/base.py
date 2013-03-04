#import threading
import multiprocessing
import re
import sys
import time
import pexpect
from dofler.config import config
from dofler.log import log

class BaseParser(multiprocessing.Process):
    '''This is the base class that all parsers inherit.  All of the process
    management is already handled here and some basic function stubs are 
    provided as a starting point for parsing the application output.
    '''
    breaker = False                 # The breaker flag.  If set to true will
                                    # cause the thread to bottom out.
    promisc = {True: '', False: ''} # The promiscuous flag settings.  As this
                                    # vary from app to app, this is set
                                    # dependent on this dictionary.
    cmd = ''                        # The child process command.
    stanza = 'Base'                 # The config file stanza name.
    #daemon = True                  # We need to make sure we daemonize.


    def run(self):
        '''The service manager for the thread.  This is where the child
        process is actually being spawned and maintained.
        '''
        start = time.time()     # Set the start timer
        interface = config.get(self.stanza, 'interface')
        timer = config.getint(self.stanza, 'timer')
        promisc = config.getboolean(self.stanza, 'promisc')

        # Replace the options in the command with the interface and promiscuous
        # settings as needed.
        cmd = self.cmd.replace('{INTERFACE}', interface)\
                      .replace('{PROMISC}', self.promisc[promisc])

        # Yeah! Loops!
        while not self.breaker:

            # Here we actually start the child process and then run through the
            # output in a loop until either the process exits, the timer hits,
            # or someone sets the breaker flag.
            p = pexpect.spawn(cmd)
            while not self.breaker and (int(time.time()) - int(start)) < timer:
                try:
                    line = p.readline()
                    #print '%s:\t%s' % (self.stanza, line.strip('\r\n'))
                    if line == '':
                        if p.isalive():
                            time.sleep(0.1)
                        else:
                            break
                    else:
                        self.parse(line)
                except pexpect.TIMEOUT:
                    pass

            # As we either broke out of the process or the timer hit, lets make
            # sure to terminate the process and reset the timer to the current
            # time.
            p.terminate()
            start = time.time()


    def parse(self, line):
        '''A simple parser for the base model'''
        print line.strip('\r\n')
