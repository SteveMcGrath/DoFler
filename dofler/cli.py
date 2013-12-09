from dofler import monitor
from dofler import common
from dofler import api
from dofler import db
from dofler.models import Setting
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
            passwd = pfile.read() 
            pfile.close()
        else:
            passwd = getpass('\nEnter Admin Password : ')
        return api.client.DoflerClient(
            '127.0.0.1', 
            common.setting('api_port').intvalue,
            'admin',
            passwd
        )
        

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
        vals = {False: 'STOPPED', True: 'RUNNING'}
        svcs = api.services()
        for item in svcs:
            print '%-20s : %s' % (item, vals[svcs[item]])


    def do_start(self, s):
        '''
        start [SERVICENAME]

        Starts the designated service. 
        '''
        api = self.getapi()
        api.start(s)


    def do_stop(self, s):
        '''
        stop [SERVICENAME]

        Stops the designated service. 
        '''
        api = self.getapi()
        api.stop(s)


    def do_restart(self, s):
        '''
        restart [SERVICENAME]

        Restarts the designated service. 
        '''
        api = self.getapi()
        api.stop(s)
        api.start(s)