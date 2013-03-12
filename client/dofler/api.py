import urllib2
import time
import Image
import MultipartPostHandler
from urllib import urlencode
from hashlib import md5
from cookielib import CookieJar
from dofler.config import config
from dofler.log import log

cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),
                              MultipartPostHandler.MultipartPostHandler())

def login():
    '''Login api.  Sends the appropriate information to get the signed cookie
    we need to be able to post to the API.
    '''

    # Lets start off and pre-populate the information we know we need.
    data = {
        'timestamp': str(time.time()),
        'username': config.get('Settings', 'sensor_name'),
    }

    # Also lets pull the information we need from the config file.
    secret = config.get('Settings', 'sensor_secret')

    # Now we will hash everything together into one nice happy hex digest and
    # then add it to the post data :)
    md5sum = md5()
    md5sum.update(data['username'])
    md5sum.update(data['timestamp'])
    md5sum.update(secret)
    data['md5hash'] = md5sum.hexdigest()

    # Then lets send everything along to the API so that we can get the cookie
    # we need.
    response = opener.open('%s/login' % config.get('Settings', 'dofler_address'), 
                           urlencode(data))


def account(username, password, info, proto, parser):
    '''account api call.  parses and uploads the account information specified
    to the dofler server.
    '''

    # First thing, if the password is more than 3 characters in length, then
    # we will obfuscate it.  We don't want to be completely brutal to the people
    # we just pwned ;)
    if len(password) >= 3:
        password = '%s%s' % (password[:3], '*' * (len(password) - 3))

    # Building the post data
    data = {
        'username': username,
        'password': password,
        'info': info,
        'proto': proto,
        'parser': parser,
    }

    # And submitting the data to the dofler server.
    opener.open('%s/post/account' % config.get('Settings', 'dofler_address'),
                urlencode(data))


def image(filename):
    '''image api call.  sends the image filename to the dofler server to be
    parsed and added to the database.
    '''
    if config.getboolean('Settings', 'client_validate'):
        try:
            image = Image.open(filename)
        except:
            return
    try:
        opener.open('%s/post/image' % config.get('Settings', 'dofler_address'),
                    {'file': open(filename), 'filetype': filename.split('.')[-1]})
    except:
        try:
            log.warn('Image %s upload failed.  Size: %s kb' %\
                     (filename, os.path.getsize(filename) / 1024))
        except:
            log.warn('Image %s doesnt exist.  Cannot upload.' % filename)


def stat(proto, count):
    '''statistical api call.  sends the json dictionary to the api for
    processing on the other end.
    '''
    # Building the post data
    data = {
        'proto': proto,
        'count': count,
    }

    # And submitting the data to the dofler server.
    opener.open('%s/post/stats' % config.get('Settings', 'dofler_address'),
                urlencode(data))