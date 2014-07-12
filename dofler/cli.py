from dofler import monitor
from dofler import common
from dofler import api
from dofler import db
from dofler import report
from dofler.models import Setting, Account, Image, Stat
from cmd import Cmd
from bottle import debug, run
from getpass import getpass
import time
import os
import sys


class CLI(Cmd):
    def getapi(self):
        '''
        Initiates a login and then returns the api client object.
        '''
        if os.path.exists(os.path.join(os.environ['HOME'], '.dofler_admin')):
            pfile = open(os.path.join(os.environ['HOME'], '.dofler_admin'))
            passwd = pfile.read().strip('\n')
            pfile.close()
        else:
            passwd = getpass('\nEnter Admin Password : ')
        return api.client.DoflerClient(
            '127.0.0.1', 
            common.setting('api_port').intvalue,
            'admin',
            passwd
        )


    def svcs_disp(self, services):
        '''
        Displays the API status. 
        '''
        vals = {False: 'STOPPED', True: 'RUNNING'}
        for service in services:
            print '%-20s : %s' % (service, vals[services[service]])

        

    def do_run(self, s):
        '''
        Runs the Dofler Service
        '''
        db.initialize()
        common.log_to_console()
        common.log_to_file()
        monitor.autostart(int(time.time()) + 5)
        debug(common.setting('api_debug').boolvalue)
        run(app=api.app,
            port=common.setting('api_port').intvalue,
            host=common.setting('api_host').value,
            server=common.setting('api_app_server').value,
            reloader=common.setting('api_debug').boolvalue,
        )


    def do_msg(self, s):
        '''
        msg MESSAGE

        Adds the specified message to the accounts captured table.
        '''
        api = self.getapi()
        api.anonymize = False
        api.account('ADMIN', 'ADMIN', s, 'ADMIN', 'MESSAGE')


    def do_report(self, s):
        '''
        report NAME 

        Generates a report with the specified name of the contents of the
        database.
        '''
        report.gen_report(s)
    
    
    def do_stats(self, s):
        '''
        stats
        
        Prints out the current statistics for the active dataset within DoFler.
        '''
        s = db.Session()
        print '\n'.join([
            '* Total Images   : %d' % s.query(Image).count(),
            '* Total Accounts : %s' % s.query(Account).count(),
        ])
    
    
    def do_accountdisp(self, s):
        '''
        accountdisp
        
        Prints all of the accounts currently stored in the database.
        '''
        s = db.Session()
        for account in s.query(Account).all():
            print '%-30s %-7s %-20s %s' % (account.info, account.proto, account.username, account.password)
    
    
    def do_imagedump(self, s):
        '''
        imagedump PATH
        
        Dumps the images from the database to disk based on last seen
        timestamp and md5sum.
        '''
        path = s
        s = Session()
        for image in s.query(Image).all():
            imgpath = '%s/%s-%s.%s' % (path, image.timestamp, image.md5sum, image.filetype)
            with open(imgpath, 'wb') as imgobj:
                imgobj.write(image.data)
                print 'Wrote %s' % imgpath


    def do_cleardb(self, s):
        '''
        cleardb

        Clears out the main database (not the settings db).  This should only
        be done while dofler is not running!
        '''
        from sqlalchemy.engine import reflection
        from sqlalchemy.schema import (MetaData, Table, DropTable, 
                                       ForeignKeyConstraint, DropConstraint)
        conn = db.engine.connect()
        trans = conn.begin()
        inspector = reflection.Inspector.from_engine(db.engine)
        metadata = MetaData(db.engine)
        metadata.reflect()
        metadata.drop_all()
        trans.commit()
        conn.close()
        vuln_db = '/opt/pvs/var/pvs/db/reports.db'
        if os.path.exists(vuln_db):
            os.system('service pvs stop')
            os.remove(vuln_db)
            os.system('service pvs start')


    def do_reset(self, s):
        '''
        reset [images|accounts]

        Clears out the current list of items on the WebUI and initiates a 30
        second timer before allowing new content to be displayed.
        '''
        api = self.getapi()
        api.reset(s)


    def do_get(self, s):
        '''
        get SETTING_NAME

        Retrieves the specified setting value and displays it to the screen.
        '''
        print common.setting(s).value


    def do_set(self, s):
        '''
        set SETTING_NAME VALUE

        Sets the specified setting to the specified value. 
        '''
        dset = s.split()
        if len(dset) == 2:
            name, value = dset
            s = db.SettingSession()
            setting = common.setting(name)
            setting.value = value
            s.merge(setting)
            s.commit()
            s.close()


    def do_list(self, s):
        '''
        list

        Lists all of the available settings. 
        '''
        s = db.SettingSession()
        for setting in s.query(Setting).all():
            print setting.name
        s.close()


    def do_services(self, s):
        '''
        services

        Lists all of the installed services and their running status. 
        '''
        api = self.getapi()
        self.svcs_disp(api.services())


    def do_start(self, s):
        '''
        start [SERVICENAME]

        Starts the designated service. 
        '''
        api = self.getapi()
        if s == 'all':
            for service in api.services():
                api.start(service)
        else:
            api.start(s)
        self.svcs_disp(api.services())


    def do_stop(self, s):
        '''
        stop [SERVICENAME]

        Stops the designated service. 
        '''
        api = self.getapi()
        if s == 'all':
            for service in api.services():
                api.stop(service)
        else:
            api.stop(s)
        self.svcs_disp(api.services())


    def do_restart(self, s):
        '''
        restart [SERVICENAME]

        Restarts the designated service. 
        '''
        api = self.getapi()
        if s == 'all':
            for service in api.services():
                api.restart(service)
        else:
            api.restart(s)
        self.svcs_disp(api.services())