from bottle import Bottle, request, response, redirect, static_file, error
from sqlalchemy.sql import func, label
from bottle.ext import sqlalchemy
from jinja2 import Environment, FileSystemLoader
from dofler import common
from dofler.common import auth, auth_login, setting
from dofler.models import *
from dofler.db import engine, Base
from dofler import monitor

env = Environment(
    lstrip_blocks=True,
    trim_blocks=True,
    loader=FileSystemLoader('/usr/share/dofler/templates')
)
app = Bottle()
plugin = sqlalchemy.Plugin(
    engine,Base.metadata, keyword='db', create=True, 
    commit=True, use_kwargs=False
)
app.install(plugin)

def get_settings_page(auth, error=False, note=False):
    return env.get_template('settings.html').render(
        error=error,
        note=note,
        auth=auth,
        status=monitor.status(),
        log_console=setting('log_console').intvalue,
        log_console_level=setting('log_console_level').value,
        log_file=setting('log_file').intvalue,
        log_file_level=setting('log_file_level').value,
        log_file_path=setting('log_file_path').value,
        api_debug=setting('api_debug').intvalue,
        api_port=setting('api_port').value,
        api_host=setting('api_host').value,
        api_app_server=setting('api_app_server').value,
        cookie_key=setting('cookie_key').value,
        server_host=setting('server_host').value,
        server_port=setting('server_port').value,
        server_ssl=setting('server_ssl').intvalue,
        server_anonymize=setting('server_anonymize').intvalue,
        server_username=setting('server_username').value,
        web_images=setting('web_images').boolvalue,
        web_accounts=setting('web_accounts').boolvalue,
        web_stats=setting('web_stats').intvalue,
        web_image_delay=setting('web_image_delay').value,
        web_account_delay=setting('web_account_delay').value,
        web_stat_delay=setting('web_stat_delay').value,
        web_stat_max=setting('web_stat_max').intvalue,
        autostart=setting('autostart').intvalue,
        ettercap_enabled=setting('ettercap_enabled').intvalue,
        driftnet_enabled=setting('driftnet_enabled').intvalue,
        tshark_enabled=setting('tshark_enabled').intvalue,
        ettercap_command=setting('ettercap_command').value,
        driftnet_command=setting('driftnet_command').value,
        tshark_command=setting('tshark_command').value,
        listen_interface=setting('listen_interface').value,
        web_account_max=setting('web_account_max').value,
        web_image_max=setting('web_image_max').value
    )

@app.get('/')
def main_page(db):
    '''
    Main View
    '''
    return env.get_template('main.html').render(
        auth=auth(request), 
        status=monitor.status(),
        web_images=setting('web_images').boolvalue,
        web_accounts=setting('web_accounts').boolvalue,
        web_stats=setting('web_stats').boolvalue,
        web_image_delay=setting('web_image_delay').intvalue,
        web_account_delay=setting('web_account_delay').intvalue,
        web_stat_delay=setting('web_stat_delay').intvalue,
        web_image_max=setting('web_image_max').intvalue,
        web_account_max=setting('web_account_max').intvalue,
        web_stat_max=setting('web_stat_max').intvalue
    )


@app.get('/static/<path:path>')
def static_files(path):
    return static_file(path, root='/usr/share/dofler/static')


@app.get('/login')
def login_page(db):
    '''
    Authentication Screen
    '''
    return env.get_template('login.html').render(
        auth=auth(request), 
        status=monitor.status()
    )


@app.post('/login')
def login_post(db):
    '''
    Authentication Handler. 
    '''
    if auth_login(request):
        response.set_cookie('user', 
            request.forms.get('username'), 
            secret=setting('cookie_key').value
        )
        response.add_header('Authentication', 'SUCCESS')
        redirect('/')
    else:
        return env.get_template('login.html').render(
            error='Authentication Failed',
            auth=False,
            status=monitor.status()
        )


@app.get('/logout')
def logout(db):
    '''
    Logout Handler.
    '''
    response.delete_cookie('user')
    redirect('/')


@app.get('/new')
def new_user_page(db):
    '''
    New User Page. 
    '''
    return env.get_template('newuser.html').render(
        auth=auth(request), 
        status=monitor.status()
    )


@app.post('/new')
def new_user_post(db):
    '''
    New User Handler. 
    '''
    if auth(request):
        db.add(User(
            request.forms.get('username'),
            request.forms.get('password')
        ))
        return eng.get_template('newuser.html').render(
            note='Account Created',
            auth=auth(request), 
            status=monitor.status()
        )
    else:
        return eng.get_template('newuser.html').render(
            error='Must be Logged in to create accounts.',
            auth=auth(request), 
            status=monitor.status()
        )


@app.get('/settings')
def settings_page(db):
    '''
    Settings Page
    '''
    return get_settings_page(auth(request))


@app.post('/settings')
def settings_post(db):
    '''
    Settings Update Handler. 
    '''
    #for item in request.forms:
    #    print item, request.forms[item]
    if auth(request):
        for item in request.forms:
            settingobj = setting(item)
            if item == 'server_password':
                if request.forms['server_password'] != '1234567890':
                    settingobj.value = request.forms[item]
            else:
                settingobj.value = request.forms[item]
            db.merge(settingobj)
        db.commit()
        common.log_to_console()
        common.log_to_file()
        monitor.autostart()
        return get_settings_page(auth(request), note='Settings Updated')
    else:
        return get_settings_page(auth(request),
            error='Must be Authenticated to Change Settings')


@app.get('/status')
def status_page(db):
    '''
    Parser Status Page. 
    '''
    return env.get_template('parsers.html').render(
        parsers=monitor.parser_status(),
        auth=auth(request), 
        status=monitor.status()
    )


@app.get('/stop/<parser>')
def stop_parser(parser, db):
    '''
    Stops the parser specified. 
    '''
    if auth(request):
        monitor.stop(parser)
        return env.get_template('parsers.html').render(
            parsers=monitor.parser_status(),
            auth=auth(request), 
            status=monitor.status()
        )
    else:
        return env.get_template('parsers.html').render(
            error='Must be Authenticated to Stop Parsers',
            parsers=monitor.parser_status(),
            auth=auth(request), 
            status=monitor.status()
        )


@app.get('/start/<parser>')
def start_parser(parser, db):
    '''
    Starts the parser specified. 
    '''
    if auth(request):
        monitor.start(parser)
        return env.get_template('parsers.html').render(
            parsers=monitor.parser_status(),
            auth=auth(request), 
            status=monitor.status()
        )
    else:
        return env.get_template('parsers.html').render(
            error='Must be Authenticated to Start Parsers',
            parsers=monitor.parser_status(),
            auth=auth(request), 
            status=monitor.status()
        )


@app.get('/restart/<parser>')
def restart_parser(parser, db):
    '''
    Stops the parser specified. 
    '''
    if auth(request):
        monitor.stop(parser)
        monitor.start(parser)
        return env.get_template('parsers.html').render(
            parsers=monitor.parser_status(),
            auth=auth(request), 
            status=monitor.status()
        )
    else:
        return env.get_template('parsers.html').render(
            error='Must be Authenticated to Restart Parsers',
            parsers=monitor.parser_status(),
            auth=auth(request), 
            status=monitor.status()
        )