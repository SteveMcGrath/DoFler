from dofler import monitor
from dofler import common
from dofler import api
from dofler import db
import time
from bottle import debug, run

def startup():
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