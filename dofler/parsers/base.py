import multiprocessing
import time
import pexpect
import psutil
from dofler.db import Session
from dofler.common import setting, log
from dofler.api.client import DoflerClient

class BaseParser(multiprocessing.Process):
    '''
    This is the base parser class that all parsers will inherit.  Basically we 
    are setting up some of the basic process management here so that we don't
    need to keep repeating it in all of the parser classes.
    '''
    name = 'base'
    delay = 0

    def run(self):
        '''
        Process startup.
        '''
        s = Session()
        while int(time.time()) < self.delay:
            log.debug('%s: Parser Waiting til %s currently %s. sleeping 1s.' %(
                self.name, self.delay, int(time.time())))
            time.sleep(1)
        self.command = setting('%s_command' % self.name).value\
                        .replace('{IF}', setting('listen_interface').value)
        self.api = DoflerClient(
            host=setting('server_host').value,
            port=setting('server_port').intvalue,
            username=setting('server_username').value,
            password=setting('server_password').value,
            ssl=setting('server_ssl').boolvalue,
            anon=setting('server_anonymize').boolvalue)
        s.close()
        self.realtime_process()


    def terminate(self):
        for process in psutil.Process(self.pid).get_children():
            process.kill()
        self.cleanup()
        multiprocessing.Process.terminate(self)


    def realtime_process(self):
        '''
        This function handles starting and stopping of the application that we
        will be interpreting the output of.  To stop a process, you need to set
        the stop flag to true, and it should cause the process to be terminated
        and the cleanup performed.
        '''
        while True:
            self.p = pexpect.spawn(self.command)
            while self.p.isalive():
                try:
                    line = self.p.readline()
                    if line == '':
                        time.sleep(0.1)
                    else:
                        self.parse(line)
                except pexpect.TIMEOUT:
                    pass


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