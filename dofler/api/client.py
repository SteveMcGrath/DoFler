import urllib2
import time
import MultipartPostHandler
from urllib import urlencode
from hashlib import md5
from cookielib import CookieJar
from dofler.config import config

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
uploader = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),
                                MultipartPostHandler.MultipartPostHandler())

def login():
    data = {
        'salt': time.time(),
        'sensor': config.get('Settings', 'sensor_name'),
    }
    secret = config.get('Settings', 'sensor_secret')
    md5sum = md5()
    md5sum.update(data['sensor'], data['salt'], secret)
    data['auth'] = md5sum.hexdigest()
    response = opener.open('%s/login' % config.get('Settings', 'dofler_address'), 
                           urlencode(data))


def account(username, password, info, proto, parser):
    data = {
        'username': username,
        'password': password,
        'info': info,
        'proto': proto,
        'parser': parser,
    }
    opener.open('%s/api/post/account' % config.get('Settings', 'dofler_address'),
                urlencode(data))


def image(filename):
    uploader.open('%s/api/post/image' % config.get('Settings', 'dofler_address'),
                  {'file': open(filename)})