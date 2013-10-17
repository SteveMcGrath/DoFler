import multiprocessing
import time
import pexpect
from dofler.log import log

class BaseParser(multiprocessing.Process):
    '''
    This is the base parser class that all parsers will inherit.  Basically we 
    are setting up some of the basic process management here so that we don't
    need to keep repeating it in all of the parser classes.
    '''
    stop = False

    def __init__(self, cmd, interface, api):
        self.command = cmd.replace('{IF}', interface)
        self.api = api


    def run(self):
        '''
        Process startup.
        '''
        self.realtime_process()


    def realtime_process(self):
        '''
        This function handles starting and stopping of the application that we
        will be interpreting the output of.  To stop a process, you need to set
        the stop flag to true, and it should cause the process to be terminated
        and the cleanup performed.
        '''
        while not self.stop:
            self.p = pexpect.spawn(cmd)
            while not self.stop:
                try:
                    line = self.p.readline()
                    if line == '':
                        if self.p.isalive():
                            time.sleep(0.1)
                        else:
                            self.stop = True
                    else:
                        self.parse(line)
                except pexpect.TIMEOUT:
                    pass
            self.p.kill(9)
        self.cleanup()


    def parse(self, line):
        '''
        Example Line parser.
        '''
        print line.strip('\r\n')


    def cleanup(self):
        '''
        Example termination cleanup.
        '''
        pass