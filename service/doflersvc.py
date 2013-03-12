from pymongo import MongoClient
import time
import json
import bleach
from bson.objectid import ObjectId
from bson.binary import Binary
from ConfigParser import ConfigParser
from hashlib import md5
from bottle import (Bottle, request, response, redirect, debug, run, 
                    static_file, error)

app = Bottle()
conn = MongoClient()
db = conn.dofler
config = ConfigParser()
config.read('/etc/dofler/service.conf')


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
    sensor = request.get_cookie('account', secret=config.get('Settings', 'key'))
    return True if sensor else False


@app.hook('before_request')
def set_json_header():
    response.set_header('Content-Type', 'application/json')
    response.set_header('Access-Control-Allow-Origin', '*')


@app.get('/static/<path:path>')
def static_files(path):
    return static_file(path, root='/usr/share/dofler')


@app.get('/')
def home_path():
    redirect('/static/viewer.html')


@app.post('/login')
def login():
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
def logout():
    '''Simply deletes the account cookie, effectively logging the sensor out.'''
    response.delete_cookie('account')


@app.post('/post/account')
def new_account():
    '''Generates a new account into the database if it doesnt already exist.'''
    if auth(request):
        data = {
            'username': bleach.clean(request.forms.get('username')),
            'password': bleach.clean(request.forms.get('password')),
            'info': bleach.clean(request.forms.get('info')),
            'proto': bleach.clean(request.forms.get('proto')),
            'parser': bleach.clean(request.forms.get('parser')),
        }
        if db.accounts.find_one(data) == None:
            db.accounts.save(data)


@app.post('/post/image')
def upload_image():
    '''Updates and/or creates a image object into the database.'''
    if auth(request):
        filedata = request.files.file.file.read()
        md5sum = md5hash(filedata)
        data = db.images.find_one({'md5': md5sum})
        if data == None:
            data = {
                'filetype': bleach.clean(request.forms.get('filetype')), 
                'data': Binary(filedata),
                'md5': md5sum,
            }
        data['timestamp'] = int(time.time())
        db.images.save(data)


@app.post('/post/stats')
def update_stats():
    '''Updates the stats database with the information posted.'''
    if auth(request):
        proto = bleach.clean(request.forms.get('proto'))
        count = bleach.clean(sint(request.forms.get('count')))
        data = db.stats.find_one({'proto': proto})
        if data == None:
            data = {
                'proto': proto,
                'count': 0,
                'trend': [],
            }
        if count != None:
            data['trend'].append(count)
            data['count'] += count
            if len(data['trend']) > config.getint('Settings', 'stat_trends'):
                del(data['trend'][0])
        db.stats.save(data)


@app.post('/post/reset/<ftype>')
def reset(ftype):
    if auth(request):
        db.resets.save({
            'collection': ftype,
            'timestamp': int(time.time())
        })
        return jsonify({'status': 'success', 'collection': ftype})


@app.get('/resets')
def ui_reset():
    resets = db.resets.find({'$gt': {'timestamp': int(time.time() - 30)}})
    data = {}
    for item in resets:
        data[item['collection']] = True
    return jsonify(data)


@app.get('/images/<timestamp:int>')
def recent_images(timestamp):
    '''
    Returns up to the last 200 images that were captured since the timestamp
    referenced.
    '''
    return jsonify(list(db.images\
                          .find({'timestamp': {'$gt': timestamp}}, {'_id': 0})\
                          .sort('timestamp', -1).limit(200)))


@app.get('/image/<md5sum>')
def get_image(md5sum):
    '''
    Returns the image from the database.
    '''
    image = db.images.find_one({'md5': md5sum})
    response.set_header('Content-Type', 'image/%s' % image['filetype'])
    return str(image['data'])


@app.get('/accounts/<oid>')
def accounts(oid):
    '''
    Returns any accounts that are newer than the oid specified.
    '''
    if oid is not '0':
        items = list(db.accounts.find({'_id': {'$gt': ObjectId(oid)}}))
    else:
        items = list(db.accounts.find())
    ilist = []
    for item in items:
        item['id'] = str(item['_id'])
        del(item['_id'])
        ilist.append(item)
    return jsonify(ilist)


@app.get('/account_total')
def account_total():
    '''
    Returns the total number of accounts stored.
    '''
    return jsonify(len(list(db.accounts.find({}))))


@app.get('/stats')
def protocol_stats():
    '''
    Returns a list of stats sorted from most prolific to least.
    '''
    return jsonify(list(db.stats.find({}, {'_id': 0}).sort({'count': -1})))


@app.get('/config')
def getconfig():
    '''
    Returns the configuration objects needed for the webUI
    '''
    return jsonify({
        'accounts': config.getboolean('WebUI', 'show_accounts'),
        'stats': config.getboolean('WebUI', 'show_stats'),
        'images': config.getboolean('WebUI', 'show_images'),
        'account_delay': config.getint('WebUI', 'account_delay'),
        'image_delay': config.getint('WebUI', 'image_delay'),
        'stats_delay': config.getint('WebUI', 'stats_delay'),
    })


def start():
    '''Starts up the service'''
    debug(config.getboolean('Settings', 'debug'))
    run(app=app,
        port=config.getint('Settings', 'port'),
        host=config.get('Settings', 'host'),
        server=config.get('Settings', 'app_server'),
        reloader=config.getboolean('Settings', 'debug')
    )