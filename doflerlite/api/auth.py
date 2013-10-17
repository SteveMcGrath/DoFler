from doflerlite.client.config import config
from bottle import (Bottle, request, response, redirect, debug, run, 
                    static_file, error)
from bottle.ext import sqlalchemy
from hashlib import md5
from dofler.models import Setting, Sensor
from dofler.common import md5hash, auth, auth_login
from dofler.db import engine, Session

app = Bottle()
plugin = sqlalchemy.Plugin(
    engine,Base.metadata, keyword='db', create=True, 
    commit=True, use_kwargs=False
)
app.install(plugin)


@app.post('/login')
def login(db):
    '''Login function'''
    if auth_login(request, db):
        response.set_cookie('user', username, secret=secret)
        response.add_header('Authentication', 'SUCCESS')
    else:
        response.add_header('Authentication', 'FAILURE')


@app.get('/logout')
def logout(db):
    '''Simply deletes the account cookie, effectively logging the sensor out.'''
    response.delete_cookie('user')