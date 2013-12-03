from dofler import monitor
from dofler import common
from dofler import api
from dofler import db
from dofler.models import Setting
import time
import sys
from cmd import Cmd
from bottle import debug, run


class CLI(Cmd):
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
        for setting in s.query(Setting).all()
            print setting.name
        s.close()


def startup():
    if len(sys.argv) > 1:
        CLI().onecmd(' '.join(sys.argv[1:]))
    else:
        CLI()