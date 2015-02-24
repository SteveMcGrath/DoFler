# -*- coding: utf-8 -*-
from bottle import Bottle, request, response, redirect, static_file, error
from sqlalchemy.sql import func, label
from sqlalchemy import desc
from bottle.ext import sqlalchemy
from dofler.common import jsonify, setting
from dofler.models import *
from dofler.db import engine, Base
import requests
import time
import sys

if sys.getdefaultencoding() != 'utf-8':  
    reload(sys)  
    sys.setdefaultencoding('utf-8')  
default_encoding = sys.getdefaultencoding()

app = Bottle()
plugin = sqlalchemy.Plugin(
    engine,Base.metadata, keyword='db', create=True, 
    commit=True, use_kwargs=False
)
app.install(plugin)

@app.hook('before_request')
def set_json_header():
    response.set_header('Content-Type', 'application/json')
    response.set_header('Access-Control-Allow-Origin', '*')


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
    images = db.query(Image).filter(Image.timestamp >= ts)\
               .order_by(desc(Image.timestamp)).limit(200).all()
    return jsonify([i.dump() for i in reversed(images)])


@app.get('/image/random')
def random_image(db):
    '''
    Returns a random image from the database.  This is MySQL-specific at the moment.
    '''
    image = db.query(Image).order_by(func.rand()).first()
    response.set_header('Content-Type', 'image/%s' % image.filetype)
    return str(image.data)



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


@app.get('/accounts/<oid:int>')
def accounts(oid, db):
    '''
    Returns any accounts that are newer than the oid specified.
    '''
    if oid is not '0':
        items = db.query(Account).filter(Account.id > oid).all()
    else:
        items = db.query(Account).limit(setting('web_image_max').intvalue).all()
    return jsonify([i.dump() for i in items])


@app.get('/stats/<limit:int>')
def stats(limit, db):
    '''
    Returns the aggregate protocol stats. 
    '''
    data = []
    protos = db.query(Stat.proto, func.sum(Stat.count))\
                .group_by(Stat.proto)\
                .order_by(desc(func.sum(Stat.count)))\
                .limit(limit).all()
    for proto in protos:
        data.append({
            'label': proto[0],
            'data': [[int(a[0] * 1000), int(a[1])] for a in db.query(Stat.timestamp, func.sum(Stat.count))\
                                            .filter(Stat.proto == proto[0])\
                                            .filter(Stat.timestamp >= int(time.time() - 10800))\
                                            .group_by(Stat.timestamp)\
                                            .order_by(desc(Stat.timestamp))\
                                            .limit(180)\
                                            .all()]
        })
    return jsonify(data)


@app.get('/vulns/<limit:int>')
def get_pvs_data(limit, db):
    '''
    Returns the top 5 vulnerable hosts as detected from the PVS sensor.
    '''
    resp = requests.post('https://%s:8835/login' % setting('pvs_host').value,
        data={
            'login': setting('pvs_user').value,
            'password': setting('pvs_password').value,
            'nocookie': 1, 'json': 1
    }, verify=False)
    pvs_key = resp.json()['reply']['contents']['token']
    data = requests.post('https://%s:8835/report2/hosts/sort' % setting('pvs_host').value, data={
        'report': 0, 'json': 1, 'token': pvs_key}, verify=False)
    hosts = data.json()['reply']['contents']['hostlist']['host']
    shosts = sorted(hosts, key=lambda k: k['severity_index'], reverse=True)
    rethosts = []
    max_vulns = 0
    for item in shosts[:limit]:
        d = {'host': item['hostname']}
        sevs = {0: 'info', 1: 'low', 2: 'medium', 3: 'high', 4: 'critical'}
        for severity in item['severitycount']['item']:
            d[sevs[severity['severitylevel']]] = severity['count']
        if item['severity'] > max_vulns:
            max_vulns = item['severity']
        rethosts.append(d)
    requests.post('https://%s:8835/logout' % setting('pvs_host').value, data={
        'seq': 1802, 'json': 1, 'token': pvs_key}, verify=False)
    return jsonify({'vuln_max': max_vulns, 'hosts': rethosts})



@app.get('/reset/<datatype>')
def reset(datatype, db):
    '''
    Returns whether a reset code has been sent in the last 30 seconds for the
    specified type of data. 
    '''
    if db.query(Reset).filter(Reset.datatype == datatype)\
                      .filter(Reset.timestamp > int(time.time()) - 30)\
                      .count() > 0:
        return jsonify(1)
    return jsonify(0)


@app.get('/settings')
def settings(db):
    '''
    Returns the settings needed for the WebUI
    '''
    return {
        'stats_enabled': setting('web_stats').boolvalue,
        'stats_delay': setting('web_stat_delay').intvalue,
        'stats_max': setting('web_stat_max').intvalue,
        'accounts_enabled': setting('web_accounts').boolvalue,
        'accounts_delay': setting('web_account_delay').intvalue,
        'accounts_max': setting('web_account_max').intvalue,
        'images_enabled': setting('web_images').boolvalue,
        'images_delay': setting('web_image_delay').intvalue,
        'images_max': setting('web_image_max').intvalue,
        'vulns_enabled': setting('web_pvs_enabled').boolvalue,
        'vulns_delay': setting('web_pvs_delay').intvalue,
        'vulns_max': setting('web_pvs_max').intvalue,
        'header_text': setting('web_header').value,
        'show_settings': setting('web_display_settings').boolvalue,
    }