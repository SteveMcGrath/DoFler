from bottle import (Bottle, request, response, redirect, debug, run, 
                    static_file, error)
from sqlalchemy.sql import func, label
from bottle.ext import sqlalchemy
from dofler.common import jsonify
from dofler.models import *
from dofler.db import engine, Session

app = Bottle()
plugin = sqlalchemy.Plugin(
    engine,Base.metadata, keyword='db', create=True, 
    commit=True, use_kwargs=False
)
app.install(plugin)

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


@app.get('/accounts/total')
def account_total(db):
    '''
    Returns the total number of accounts stored.
    '''
    return jsonify(db.query(Account).count())


@app.get('/accounts/<int:oid>')
def accounts(oid, db):
    '''
    Returns any accounts that are newer than the oid specified.
    '''
    if oid is not '0':
        items = db.query(Account).filter(Account.id > oid).all()
    else:
        items = db.query(Account).all()
    return jsonify([i.dump() for i in items])


@app.get('/stats/<int:limit>')
def stats(limit, db):
    '''
    Returns the aggregate protocol stats. 
    '''
    data = {}
    protos = db.query(Protocol).order_by(Protocol.total).limit(limit).all()
    for proto in protos:
        data[proto.name] = proto.history(180)
    return jsonify(data)

