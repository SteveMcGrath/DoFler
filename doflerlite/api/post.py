from bottle import (Bottle, request, response, redirect, debug, run, 
                    static_file, error)
from bottle.ext import sqlalchemy
from dofler.api.auth import auth
from dofler.common import md5hash
from dofler.models import *
from dofler.db import engine, Session

app = Bottle()
plugin = sqlalchemy.Plugin(
    engine,Base.metadata, keyword='db', create=True, 
    commit=True, use_kwargs=False
)
app.install(plugin)


@app.post('/account')
def new_account(db):
    '''Generates a new account into the database if it doesnt already exist.'''
    if auth(request, db):
        username = request.forms.get('username'),
        password = request.forms.get('password'),
        info = request.forms.get('info'),
        proto = request.forms.get('proto'),
        parser = request.forms.get('parser'),
        try:
            account = db.query(Account).filter_by(username=username,
                                                 proto=proto,
                                                 password=password,
                                                 info=info).one()
        except:
            account = Account(username, password, info, proto, parser)
            db.add(account)


@app.post('/image')
def upload_image(db):
    '''Updates and/or creates a image object into the database.'''
    if auth(request, db):
        filedata = request.files.file.file.read()
        md5sum = md5hash(filedata)
        try:
            image = db.query(Image).filter_by(md5sum=md5sum).one()
            image.timestamp = int(time.time())
            image.count += 1
            db.merge(image)
        except:
            image = Image(int(time.time()), 
                          bleach.clean(request.forms.get('filetype')),
                          filedata
            )
            db.add(image)


@app.post('/stat')
def upload_stat(db):
    '''Uploads new statistics to the database.'''
    if auth(request, db):
        sensor = request.forms.get('sensor')
        proto = request.forms.get('proto')
        count = int(request.forms.get('count'))
        stat = Stat(sensor, proto, count)
        if db.query(Protocol).filter_by(name=proto).count() < 1:
            db.add(Protocol(proto))
        db.add(stat)
