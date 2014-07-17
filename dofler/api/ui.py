from bottle import Bottle, request, response, redirect, static_file, error
from sqlalchemy.sql import func, label
from bottle.ext import sqlalchemy
import markdown
from jinja2 import Environment, FileSystemLoader
from ConfigParser import ConfigParser
from dofler import get_version_info
from dofler import config
from dofler import common
from dofler.common import auth, auth_login, setting
from dofler.models import *
from dofler.db import engine, Base, SettingSession
from dofler import monitor
import os
import sys

if os.name == 'nt':
    DATA_PREFIX = os.path.dirname(sys.executable) + '\\share\\dofler\\'
else:
    DATA_PREFIX = "/".join(os.path.dirname(sys.executable).split("/")[:-1]) + '/share/dofler/'

env = Environment(
    lstrip_blocks=True,
    trim_blocks=True,
    loader=FileSystemLoader(DATA_PREFIX + 'templates')
)
app = Bottle()
plugin = sqlalchemy.Plugin(
    engine,Base.metadata, keyword='db', create=True, 
    commit=True, use_kwargs=False
)
app.install(plugin)


def update_settings(settings):
    '''
    Settings Updater 
    '''
    s = SettingSession()
    for item in settings:
        if item == 'database':
            config.update(settings[item])
        else:
            settingobj = setting(item)
            if item == 'server_password':
                if settings[item] != '1234567890':
                    settingobj.value = settings[item]
            else:
                settingobj.value = settings[item]
            s.merge(settingobj)
    s.commit()
    s.close()
    common.log_to_console()
    common.log_to_file()
    monitor.autostart()


@app.get('/')
def main_page(db):
    '''
    Main View
    '''
    return env.get_template('themes/%s.html' % setting('web_theme').value).render()


@app.get('/static/<path:path>')
def static_files(path):
    return static_file(path, root=DATA_PREFIX + 'static')


@app.get('/settings')
def settings_page(db):
    '''
    Settings Page
    '''
    return env.get_template('settings_base.html').render(
        auth=auth(request),
        vinfo=get_version_info()
    )


@app.get('/settings/docs')
@app.get('/settings/docs/<path:path>')
def documentation(db, path=None):
    '''
    Documentation Pages.
    '''
    data = None
    if path:
        try:
            with open(DATA_PREFIX + 'docs/%s.md' % path) as mdfile:
                data = markdown.markdown(mdfile.read(), extensions=[
                    'codehilite',
                    'extra',
                ])
        except:
            pass
    return env.get_template('settings_doc_page.html').render(
        auth=auth(request),
        doc_content=data
    )




@app.get('/settings/login')
@app.post('/settings/login')
def login(db):
    '''
    Authentication Page
    '''
    error=None
    logged_in=False
    if request.method == 'POST':
        if auth_login(request):
            response.set_cookie('user', 
                request.forms.get('username'), 
                secret=setting('cookie_key').value,
            )
            response.add_header('Authentication', 'SUCCESS')
            logged_in=True
        else:
            error='Authentication Failed'
    else:
        logged_in=auth(request)
    return env.get_template('settings_login.html').render(
        auth=logged_in,
        error=error
    )


@app.post('/settings/logout')
def logout(db):
    '''
    User Logout. 
    '''
    response.delete_cookie('user',
        secret=setting('cookie_key').value)
    return env.get_template('settings_login.html').render(
        auth=False,
    )


@app.get('/settings/users')
@app.post('/settings/users')
def user_settings(db):
    '''
    User Management Page
    '''
    s = SettingSession()
    if auth(request) and request.method == 'POST':
        username = request.forms.get('username')
        password = request.forms.get('password')
        action = request.forms.get('action')
        if action == 'Create':
            s.add(User(username, password))
        if action == 'Update':
            user = s.query(User).filter_by(name=username).one()
            user.update(password)
            s.merge(user)
        if action == 'Remove' and username != 'admin':
            user = s.query(User).filter_by(name=username).one()
            s.delete(user)
        s.commit()
    users = s.query(User).all()
    s.close()
    return env.get_template('settings_users.html').render(
        auth=auth(request),
        users=users
    )


@app.get('/settings/api')
@app.post('/settings/api')
def api_settings(db):
    '''
    API Settings Page 
    '''
    if auth(request) and request.method == 'POST':
        settings = {}
        for item in request.forms:
            settings[item] = request.forms[item]
        update_settings(settings)
    return env.get_template('settings_api.html').render(
        auth=auth(request),
        api_debug=setting('api_debug').intvalue,
        api_port=setting('api_port').value,
        api_host=setting('api_host').value,
        api_app_server=setting('api_app_server').value,
        cookie_key=setting('cookie_key').value,
        database=config.config.get('Database', 'db')
    )


@app.get('/settings/server')
@app.post('/settings/server')
def api_settings(db):
    '''
    Server Settings Page 
    '''
    if auth(request) and request.method == 'POST':
        settings = {}
        for item in request.forms:
            settings[item] = request.forms[item]
        update_settings(settings)
    return env.get_template('settings_server.html').render(
        auth=auth(request),
        server_host=setting('server_host').value,
        server_port=setting('server_port').value,
        server_ssl=setting('server_ssl').intvalue,
        server_anonymize=setting('server_anonymize').intvalue,
        server_username=setting('server_username').value
    )


@app.get('/settings/logging')
@app.post('/settings/logging')
def api_settings(db):
    '''
    Logging Settings Page 
    '''
    if auth(request) and request.method == 'POST':
        settings = {}
        for item in request.forms:
            settings[item] = request.forms[item]
        update_settings(settings)
    return env.get_template('settings_logging.html').render(
        auth=auth(request),
        log_console=setting('log_console').intvalue,
        log_console_level=setting('log_console_level').value,
        log_file=setting('log_file').intvalue,
        log_file_level=setting('log_file_level').value,
        log_file_path=setting('log_file_path').value
    )


@app.get('/settings/webui')
@app.post('/settings/webui')
def api_settings(db):
    '''
    WebUI Settings Page 
    '''
    if auth(request) and request.method == 'POST':
        settings = {}
        for item in request.forms:
            settings[item] = request.forms[item]
        update_settings(settings)
    return env.get_template('settings_webui.html').render(
        auth=auth(request),
        web_images=setting('web_images').boolvalue,
        web_accounts=setting('web_accounts').boolvalue,
        web_stats=setting('web_stats').intvalue,
        web_image_delay=setting('web_image_delay').value,
        web_account_delay=setting('web_account_delay').value,
        web_stat_delay=setting('web_stat_delay').value,
        web_stat_max=setting('web_stat_max').intvalue,
        web_image_max=setting('web_image_max').intvalue,
        web_account_max=setting('web_account_max').intvalue,
        web_display_settings=setting('web_display_settings').boolvalue
    )


@app.get('/settings/services')
@app.post('/settings/services')
def services_settings(db):
    '''
    Services Status Page 
    '''
    if auth(request) and request.method == 'POST':
        parser = request.forms.get('parser')
        action = request.forms.get('action')
        if action == 'Stop':
            monitor.stop(parser)
        if action == 'Start':
            monitor.start(parser)
        if action == 'Restart':
            monitor.stop(parser)
            monitor.start(parser)
    return env.get_template('settings_services.html').render(
        auth=auth(request),
        parsers=monitor.parser_status()
    )


@app.get('/settings/parsers')
@app.post('/settings/parsers')
def parsers_settings(db):
    '''
    Parser Configuration Settings Page
    '''
    if auth(request) and request.method == 'POST':
        settings = {}
        for item in request.forms:
            settings[item] = request.forms[item]
        update_settings(settings)
    parsers = {}
    for item in monitor.parser_status():
        parsers[item] = {
            'enabled': setting('%s_enabled' % item).boolvalue,
            'command': setting('%s_command' % item).value,
        }
    return env.get_template('settings_parsers.html').render(
        auth=auth(request),
        parsers=parsers,
        autostart=setting('autostart').boolvalue,
        listen_interface=setting('listen_interface').value
    )