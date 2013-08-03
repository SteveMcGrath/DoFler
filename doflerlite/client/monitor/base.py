#import threading
import multiprocessing
import re
import sys
import time
import pexpect
from doflerlite.client.config import config
from doflerlite.client.log import log

class BaseParser(multiprocessing.Process):
    '''
    This is the base class that all parsers inherit.  All of the process
    management is already handled here and some basic function stubs are 
    provided as a starting point for parsing the application output.
    '''
    breaker = False                 # - The breaker flag.  If set to true will
                                    # cause the thread to bottom out.

    promisc = {True: '', False: ''} # - The promiscuous flag settings.  As this
                                    #   vary from app to app, this is set
                                    #   dependent on this dictionary.
    cmd = ''                        # - The child process
    rt_args = ''                    # - What args will be run in realtime mode
    ring_args = ''                  # - What args will be run in ringbuffer mode
    stanza = 'Base'                 # - The config file stanza name.
    realtime = True                 # - Are we running this parser in realtime
                                    # or not?
    pcap_file =None                 # - This is used in ringbuffer mode.
                                    #   Basically the path/filename of the pcap.


    def run(self):
        '''
        The service manager for the thread.  This is where the child
        process is actually being spawned and maintained.
        '''
        if self.realtime:
            self.realtime_process()
        else:
            self.ringbuffer_process()


    def realtime_process(self):
        '''
        Realtime process manager.
        '''
        interface = config.get('Parser: %s' % self.stanza, 'interface')
        promisc = config.getboolean('Parser: %s' % self.stanza, 'promisc')

        # First thing we need to compile the command that we will be using
        # We will be combining the base command with the arguments specified.
        cmd = self.cmd.replace('{INTERFACE}', interface)\
                        .replace('{PROMISC}', self.promisc[promisc])

        # Instead of mentioning it over and over again, its worth pointing out
        # that you will be seeing the breaker variable many times within this
        # block of code.  If the process needs to be stopped for whatever reason
        # this variable acts as the flag to initiate that shutdown of the
        # process.
        while not self.breaker:
            # Lets spawn the process
            p = pexpect.spawn(cmd)
            while not self.breaker:
                try:
                    line = p.readline()
                    if line == '':
                        if p.isalive():
                            time.sleep(0.1)
                        else:
                            self.breaker = True
                    else:
                        self.parse(line)
                except pexpect.TIMEOUT:
                    pass
            p.kill(9)


    def ringbuffer_process(self):
        '''
        Ringbuffer (offline) process manager.
        '''

        # First thing we need to compile the command that we will be using
        # We will be combining the base command with the arguments specified.
        cmd = '%s %s' % (self.cmd, 
            self.ring_args.replace('{PCAP}', self.pcap_file))
        p = pexpect.spawn(cmd)
        while p.isalive():
            line = p.readline()
            if line == '':
                time.sleep(0.1)
            else:
                self.parse(line)


    def parse(self, line):
        '''A simple parser for the base model'''
        print line.strip('\r\n')
