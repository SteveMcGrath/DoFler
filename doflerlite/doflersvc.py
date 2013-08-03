import time
import json
import bleach
from ConfigParser import ConfigParser
from hashlib import md5
import client
from doflerlite.client.config import config
from bottle import (Bottle, request, response, redirect, debug, run, 
                    static_file, error)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, Text, LargeBinary, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from bottle.ext import sqlalchemy

app = Bottle()
Base = declarative_base()
engine = create_engine(config.get('Database', 'path'))
Session = sessionmaker(bind=engine)

plugin = sqlalchemy.Plugin(
    engine,Base.metadata, keyword='db', create=True, 
    commit=True, use_kwargs=False
)
app.install(plugin)


class Account(Base):
    __tablename__ = 'accounts'
    id = Column(Integer, primary_key=True)
    username = Column(Text)
    password = Column(Text)
    info = Column(Text)
    proto = Column(Text)
    parser = Column(Text)

    def __init__(self, username, password, info, proto, parser):
        self.username = username
        self.password = password
        self.info = info
        self.proto = proto
        self.parser = parser

    def dump(self):
        return {
            'username': self.username,
            'password': self.password,
            'info': self.info,
            'proto': self.proto,
            'parser': self.parser,
        }
Account.metadata.create_all(engine)


class Image(Base):
    __tablename__ = 'images'
    md5sum = Column(Text, primary_key=True)
    timestamp = Column(Integer)
    data = Column(LargeBinary)
    filetype = Column(Text)
    count = Column(Integer)

    def __init__(self, timestamp, filetype, data):
        self.md5sum = md5hash(data)
        self.timestamp = timestamp
        self.filetype = filetype
        self.data = data
        self.count = 1

    def dump(self):
        return {
            'md5sum': self.md5sum,
            'timestamp': self.timestamp,
            'count': self.count,
        }
Image.metadata.create_all(engine)


def ignore_exception(IgnoreException=Exception,DefaultVal=None):
    ''' Decorator for ignoring exception from a function
    e.g.   @ignore_exception(DivideByZero)
    e.g.2. ignore_exception(DivideByZero)(Divide)(2/0)
    From: sharjeel
    Source: stackoverflow.com
    '''
    def dec(function):
        def _dec(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except IgnoreException:
                return DefaultVal
        return _dec
    return dec
sint = ignore_exception(ValueError)(int)


def md5hash(*items):
    '''md5hash list, of, items
    A simple convenience function to return a hex md5hash of all of the
    items given.
    '''
    m = md5()
    for item in items:
        m.update(str(item))
    return m.hexdigest()


def jsonify(data):
    '''A simple shortcut for dumping json dictionaries.  This can come in handy
    if we need to make some global settings for how to return json data.
    '''
    return json.dumps(data)


def auth(request):
    '''Returns True or False based on if the account cookie is set.'''
    #sensor = request.get_cookie('account', secret=config.get('Settings', 'key'))
    #return True if sensor else False
    return True


@app.hook('before_request')
def set_json_header():
    response.set_header('Content-Type', 'application/json')
    response.set_header('Access-Control-Allow-Origin', '*')


@app.get('/static/<path:path>')
def static_files(path, db):
    return static_file(path, root='/usr/share/dofler')


@app.get('/')
def home_path(db):
    redirect('/static/viewer.html')


@app.post('/login')
def login(db):
    '''Login function'''
    loggedin = False
    if not auth(request):
        mhash = bleach.clean(request.forms.get('md5hash'))
        timestamp = bleach.clean(request.forms.get('timestamp'))
        username = bleach.clean(request.forms.get('username'))
        newhash = md5hash(username, timestamp, config.get(username, 'secret'))
        if mhash == newhash:
            loggedin = True
            response.set_cookie('account', username,
                                secret=config.get('Settings', 'key'))
    if not loggedin:
        response.set_header('Login Status', 'FAILED')


@app.get('/logout')
def logout(db):
    '''Simply deletes the account cookie, effectively logging the sensor out.'''
    response.delete_cookie('account')


@app.post('/post/account')
def new_account(db):
    '''Generates a new account into the database if it doesnt already exist.'''
    if auth(request):
        username = bleach.clean(request.forms.get('username')),
        password = bleach.clean(request.forms.get('password')),
        info = bleach.clean(request.forms.get('info')),
        proto = bleach.clean(request.forms.get('proto')),
        parser = bleach.clean(request.forms.get('parser')),
        try:
            account = db.query(Account).filter_by(username=username,
                                                 proto=proto,
                                                 password=password,
                                                 info=info).one()
        except:
            account = Account(username, password, info, proto, parser)
            s.add(account)
        s.commit()


@app.post('/post/image')
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
                          bleach.clean(request.forms.get('filetype')),
                          filedata
            )
            db.add(image)


@app.get('/images/<ts:int>')
def recent_images(ts, db):
    '''
    Returns up to the last 200 images that were captured since the timestamp
    referenced.
    '''
    if ts == 0:
        skippr = db.query(Image).count() - 200
        if skippr < 0:
            skippr = 0
    else:
        skippr = 0
    return jsonify([i.dump() for i in db.query(Image)\
                                        .filter(Image.timestamp > ts)\
                                        .offset(skippr).all()])


@app.get('/image/<md5sum>')
def get_image(md5sum, db):
    '''
    Returns the image from the database.
    '''
    try:
        image = db.query(Image).filter_by(md5sum=md5sum).one()
    except:
        image = Image(0,'jpg','')
    response.set_header('Content-Type', 'image/%s' % image.filetype)
    return str(image.data)


@app.get('/accounts/<oid>')
def accounts(oid, db):
    '''
    Returns any accounts that are newer than the oid specified.
    '''
    if oid is not '0':
        items = db.query(Account).filter(Account.id > oid).all()
    else:
        items = db.query(Account).all()
    return jsonify([i.dump() for i in items])


@app.get('/account_total')
def account_total(db):
    '''
    Returns the total number of accounts stored.
    '''
    return jsonify(db.query(Account).count())


@app.get('/config')
def getconfig(db):
    '''
    Returns the configuration objects needed for the webUI
    '''
    return jsonify({
        'accounts': config.getboolean('WebUI', 'show_accounts'),
        'stats': False,
        'images': config.getboolean('WebUI', 'show_images'),
        'account_delay': config.getint('WebUI', 'account_delay'),
        'image_delay': config.getint('WebUI', 'image_delay'),
        'stats_delay': 999,
    })


def start():
    '''Starts up the service'''
    client.start()
    debug(config.getboolean('WebServer', 'debug'))
    run(app=app,
        port=config.getint('WebServer', 'port'),
        host=config.get('WebServer', 'host'),
        server=config.get('WebServer', 'app_server'),
        reloader=config.getboolean('WebServer', 'debug')
    )