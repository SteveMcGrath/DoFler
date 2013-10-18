from bottle import (Bottle, request, response, redirect, debug, run, 
                    static_file, error)
from sqlalchemy.sql import func, label
from bottle.ext import sqlalchemy
from jinja2 import Environment, FileSystemLoader
from dofler.common import auth, auth_login, setting
from dofler.models import *
from dofler.db import engine, Session
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

@app.get('/')
def main_page(db):
    '''
    Main View
    '''
    return env.get_template('home.html').render(
        auth=auth(request, db), 
        status=monitor.status(),
        web_images=setting('web_images', db).boolvalue,
        web_accounts=setting('web_accounts', db).boolvalue,
        web_stats=setting('web_stats', db).boolvalue,
        web_image_delay=setting('web_image_delay', db).intvalue,
        web_account_delay=setting('web_account_delay', db).intvalue,
        web_stat_delay=setting('web_stat_delay', db).intvalue,
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
        auth=auth(request, db), 
        status=monitor.status()
    )


@app.post('/login')
def login_post(db):
    '''
    Authentication Handler. 
    '''
    if auth_login(request, db):
        redirect('/')
    else:
        env.get_template('login.html').render(
            error='Authentication Failed',
            auth=auth(request, db), 
            status=monitor.status()
        )


@app.get('/new')
def new_user_page(db):
    '''
    New User Page. 
    '''
    return eng.get_template('newuser.html').render(
        auth=auth(request, db), 
        status=monitor.status()
    )


@app.post('/new')
def new_user_post(db):
    '''
    New User Handler. 
    '''
    if auth(request, db):
        db.add(User(
            request.forms.get('username'),
            request.forms.get('password')
        ))
        return eng.get_template('newuser.html').render(
            note='Account Created'
            auth=auth(request, db), 
            status=monitor.status()
        )
    else:
        return eng.get_template('newuser.html').render(
            error='Must be Logged in to create accounts.'
            auth=auth(request, db), 
            status=monitor.status()
        )


@app.get('/settings')
def settings_page(db):
    '''
    Settings Page
    '''
    return env.get_template('settings.html').render(
        auth=auth(request, db), 
        status=monitor.status(),
        log_console=setting('log_console', db).boolvalue,
        log_console_level=setting('log_console_level', db).value,
        log_file=setting('log_file', db).boolvalue,
        log_file_level=setting('log_file_level', db).value,
        log_file_path=setting('log_file_path', db).value,
        api_debug=setting('api_debug', db).boolvalue,
        api_port=setting('api_port', db).value,
        api_host=setting('api_host', db).value,
        api_ssl=setting('api_ssl', db).boolvalue,
        api_app_server=setting('api_app_server', db).value,
        server_host=setting('server_host', db).value,
        server_port=setting('server_port', db).value,
        server_ssl=setting('server_ssl', db).boolvalue,
        server_anonymize=setting('server_anonymize', db).boolvalue,
        server_username=setting('server_username', db).value,
        web_images=setting('web_images', db).boolvalue,
        web_accounts=setting('web_accounts', db).boolvalue,
        web_stats=setting('web_stats', db).boolvalue,
        web_image_delay=setting('web_image_delay', db).value,
        web_account_delay=setting('web_account_delay', db).value,
        web_stat_delay=setting('web_stat_delay', db).value,
        autostart=setting('autostart', db).boolvalue,
        ettercap_enabled=setting('ettercap_enabled', db).boolvalue,
        driftnet_enabled=setting('driftnet_enabled', db).boolvalue,
        tshark_enabled=setting('tshark_enabled', db).boolvalue,
        ettercap_command=setting('ettercap_command', db).value,
        driftnet_command=setting('driftnet_command', db).value,
        tshark_command=setting('tshark_command', db).value,
    )


@app.post('/settings')
def settings_post(db):
    '''
    Settings Update Handler. 
    '''
    if auth(request, db):
        for item in request.forms:
            settingobj = setting(item)
            settingobj.value = request.forms[item]
            db.merge(settingobj)
        return env.get_template('settings.html').render(note='Settings Updated')
    else:
        return env.get_template('settings.html').render(
            error='Must be Authenticated to Change Settings',
            auth=auth(request, db), 
            status=monitor.status()
        )


@app.get('/status')
def status_page(db):
    '''
    Parser Status Page. 
    '''
    return env.get_template('status.html').render(
        parsers=monitor.parser_status(),
        auth=auth(request, db), 
        status=monitor.status()
    )


@app.post('/stop')
def stop_parser(db):
    '''
    Stops the parser specified. 
    '''
    if auth(request, db):
        monitor.stop(request.forms.get('parser'))
        return env.get_template('status.html').render(
            parsers=monitor.parser_status(),
            auth=auth(request, db), 
            status=monitor.status()
        )
    else:
        return env.get_template('status.html').render(
            error='Must be Authenticated to Stop Parsers',
            parsers=monitor.parser_status(),
            auth=auth(request, db), 
            status=monitor.status()
        )


@app.post('/start')
def start_parser(db):
    '''
    Starts the parser specified. 
    '''
    if auth(request, db):
        monitor.start(request.forms.get('parser'))
        return env.get_template('status.html').render(
            parsers=monitor.parser_status(),
            auth=auth(request, db), 
            status=monitor.status()
        )
    else:
        return env.get_template('status.html').render(
            error='Must be Authenticated to Start Parsers'
            parsers=monitor.parser_status(),
            auth=auth(request, db), 
            status=monitor.status()
        )


@app.post('/restart')
def restart_parser(db):
    '''
    Stops the parser specified. 
    '''
    if auth(request, db):
        monitor.stop(request.forms.get('parser'))
        monitor.start(request.forms.get('parser'))
        return env.get_template('status.html').render(
            parsers=monitor.parser_status(),
            auth=auth(request, db), 
            status=monitor.status()
        )
    else:
        return env.get_template('status.html').render(
            error='Must be Authenticated to Restart Parsers',
            parsers=monitor.parser_status(),
            auth=auth(request, db), 
            status=monitor.status()
        )