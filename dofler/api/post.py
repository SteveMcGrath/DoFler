from bottle import Bottle, request, response, redirect, static_file, error
from bottle.ext import sqlalchemy
from dofler.api.auth import auth
from dofler.common import md5hash, jsonify
from dofler.models import *
from dofler.db import engine, Base
from dofler import monitor

app = Bottle()
plugin = sqlalchemy.Plugin(
    engine,Base.metadata, keyword='db', create=True, 
    commit=True, use_kwargs=False
)
app.install(plugin)


@app.post('/account')
def new_account(db):
    '''Generates a new account into the database if it doesnt already exist.'''
    if auth(request):
        username = str(request.forms.get('username')),
        password = str(request.forms.get('password')),
        info = str(request.forms.get('info')),
        proto = str(request.forms.get('proto')),
        parser = str(request.forms.get('parser')),
        if isinstance(username, tuple): username = username[0]
        if isinstance(password, tuple): password = password[0]
        if isinstance(info, tuple): info = info[0]
        if isinstance(proto, tuple): proto = proto[0]
        if isinstance(parser, tuple): parser = parser[0]
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
    if auth(request):
        filedata = request.files.file.file.read()
        md5sum = md5hash(filedata)
        try:
            image = db.query(Image).filter_by(md5sum=md5sum).one()
            image.timestamp = int(time.time())
            image.count += 1
            db.merge(image)
        except:
            image = Image(int(time.time()), 
                          request.forms.get('filetype'),
                          filedata
            )
            db.add(image)


@app.post('/stat')
def upload_stat(db):
    '''Uploads new statistics to the database.'''
    if auth(request):
        username = request.forms.get('username')
        proto = request.forms.get('proto')
        count = int(request.forms.get('count'))
        if isinstance(username, tuple): sensor = sensor[0]
        if isinstance(proto, tuple): proto = proto[0]
        db.add(Stat(proto, username, count))


@app.post('/reset')
def push_reset(db):
    '''
    Pushes a reset into the DB to clear out any undesirable data from the UI. 
    '''
    if auth(request):
        db.add(Reset(request.forms.get('type')))


@app.post('/services')
def services(db):
    '''
    Returns the running status of the services on the dofler sensor. 
    '''
    return jsonify(monitor.parser_status())