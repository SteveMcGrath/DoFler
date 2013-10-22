from base import BaseParser, log
import re
import os

class Parser(BaseParser):
    '''
    Driftnet Parser.  This parser interprets the output of driftnet run in
    headless mode and will pickup the files that have been dropped on the
    disk.  Once sent to the api, we will remove the temporary file.  This should
    help keep the overall cruft on disk to a minimum.
    '''
    name = 'driftnet'

    def parse(self, line):
        '''
        Driftnet output line parser. 
        '''
        # This parser is about as simple as they come.  Every line is simply a
        # filename of the image that driftnet carved out.  All we need to do is
        # open it up, send the data to the API, then remove the file.
        filename = line.strip('\r\n ')
        log.debug('DRIFTNET: sending image %s' % filename)
        self.api.image(filename)
        try:
            os.remove(filename)
        except:
            log.warn('DRIFTNET: could not remove %s' % filename)


    def cleanup(self):
        '''
        Process cleanup.
        '''
        # Driftnet doesnt always clean up after itself, so here we will look to
        # see if the process is running, and if it isnt, then cleanup the
        # pidfile if it exists.
        pidfile = '/var/run/driftnet.pid'
        if os.path.exists(pidfile):
            try:
                os.kill(int(open(pidfile).read()), 0)
            except OSError, e:
                log.error('DRIFTNET: Cannot kill driftnet pidfile, still alive.')
            else:
                os.remove(pidfile)