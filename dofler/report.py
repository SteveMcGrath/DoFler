from dofler.models import *
from dofler.db import Session
from dofler.api.ui import env
from sqlalchemy.sql import func, label
from sqlalchemy import desc
import collections
import base64
import json
import time
import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_timestamp(string, end=False):
    year, month, day = string.split('-')
    year = int(year)
    month = int(month)
    day = int(day)
    if end:
        hour = 23
        minute = 59
        second = 59
    else:
        hour = 0
        minute = 0
        second = 0
    return int(time.mktime(\
                datetime.datetime(year, month, day, hour, minute, second).utctimetuple()))


def get_stats(limit):
    s = Session()
    data = []
    protos = s.query(Stat.proto, func.sum(Stat.count))\
                .group_by(Stat.proto)\
                .order_by(desc(func.sum(Stat.count)))\
                .limit(limit).all()
    for proto in protos:
        data.append({
            'label': proto[0],
            'data': [[int(a[0] * 1000), int(a[1])] for a in s.query(Stat.timestamp, func.sum(Stat.count))\
                                            .filter(Stat.proto == proto[0])\
                                            .group_by(Stat.timestamp)\
                                            .order_by(desc(Stat.timestamp))\
                                            .all()]
        })
    s.close()
    return data


def gen_report(title):
    s = Session()
    
    # New Unique Image Counts over the course of the day.
    trend = {}
    for image in s.query(Image).all():
        dts = datetime.datetime.fromtimestamp(image.timestamp)
        hrtime = int(time.mktime((dts.year, dts.month, dts.day, dts.hour, 0, 0, 0, 0, 0)))
        if hrtime not in trend:
            trend[hrtime] = 0
        trend[hrtime] += 1
    od = collections.OrderedDict(sorted(trend.items()))
    itrend = [{'data': [[i * 1000, od[i]] for i in od], 'label': 'Unique Images'}]

    # Top 10 Most common images
    top100 = s.query(Image).order_by(desc(Image.count)).limit(100).all()

    # Total Unique Images
    total_images = s.query(Image).count()

    # accounts
    accounts = s.query(Account).all()

    # Stats
    proto_top10 = get_stats(10)
    protos = s.query(Stat.proto, func.sum(Stat.count))\
                .group_by(Stat.proto)\
                .order_by(desc(func.sum(Stat.count))).all()

    report = env.get_template('report.html').render(
        title = title,
        accounts = accounts,
        itrend = json.dumps(itrend),
        itop = top100,
        itotal = total_images,
        pt10 = json.dumps(proto_top10),
        protos = protos,
        jquery = '\n'.join([
            open('/usr/share/dofler/static/jquery.min.js').read(),
            open('/usr/share/dofler/static/jquery.flot.min.js').read(),
            open('/usr/share/dofler/static/jquery.flot.time.min.js').read(),
        ]).encode('utf-8')
    )
    with open('DoFler-%s.html' % title.replace(' ','_'), 'w') as reportfile:
        reportfile.write(report)
    s.close()


def image_dump(path):
    s = Session()
    for image in s.query(Image).all():
        with open(path + '/%d-%s.%s' %\
                  (image.timestamp, image.md5sum, image.filetype), 'w') as ifile:
            ifile.write(image.data)
        print 'Dumped : %d-%s.%s' % (image.timestamp, image.md5sum, image.filetype)
    s.close()