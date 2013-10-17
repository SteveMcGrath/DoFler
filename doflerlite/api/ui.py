from bottle import (Bottle, request, response, redirect, debug, run, 
                    static_file, error)
from sqlalchemy.sql import func, label
from bottle.ext import sqlalchemy
from jinja2 import Environment, FileSystemLoader
from dofler.common import auth, auth_login
from dofler.models import *
from dofler.db import engine, Session
from dofler import monitor

env = Environment(loader=FileSystemLoader('/usr/share/dofler/templates'))
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
        auth=auth, 
        status=monitor.status(),
        web_images=db.query(Setting).filter_by(name='web_images').boolvalue,
        web_accounts=db.query(Setting).filter_by(name='web_accounts').boolvalue,
        web_stats=db.query(Setting).filter_by(name='web_stats').boolvalue,
        web_image_delay=db.query(Setting).filter_by(name='web_image_delay').intvalue,
        web_account_delay=db.query(Setting).filter_by(name='web_account_delay').intvalue,
        web_stat_delay=db.query(Setting).filter_by(name='web_stat_delay').intvalue,
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
        auth=auth, 
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
            auth=auth, 
            status=monitor.status()
        )


@app.get('/settings')
def settings_page(db):
    '''
    Settings Page
    '''
    return env.get_template('settings.html').render(
        auth=auth, 
        status=monitor.status()
    )


@app.post('/settings')
def settings_post(db):
    '''
    Settings Update Handler. 
    '''
    if auth(request, db):
        for item in request.forms:
            setting = db.query(Setting).filter_by(name=item).one()
            setting.value = request.forms[item]
            db.merge(setting)
        return env.get_template('settings.html').render(note='Settings Updated')
    else:
        return env.get_template('settings.html').render(
            error='Must be Authenticated to Change Settings',
            auth=auth, 
            status=monitor.status()
        )


@app.get('/status')
def status_page(db):
    '''
    Parser Status Page. 
    '''
    return env.get_template('status.html').render(
        parsers=monitor.parser_status(),
        auth=auth, 
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
            auth=auth, 
            status=monitor.status()
        )
    else:
        return env.get_template('status.html').render(
            error='Must be Authenticated to Stop Parsers',
            parsers=monitor.parser_status(),
            auth=auth, 
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
            auth=auth, 
            status=monitor.status()
        )
    else:
        return env.get_template('status.html').render(
            error='Must be Authenticated to Start Parsers'
            parsers=monitor.parser_status(),
            auth=auth, 
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
            auth=auth, 
            status=monitor.status()
        )
    else:
        return env.get_template('status.html').render(
            error='Must be Authenticated to Restart Parsers',
            parsers=monitor.parser_status(),
            auth=auth, 
            status=monitor.status()
        )