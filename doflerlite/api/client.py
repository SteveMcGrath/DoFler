import urllib2
import time
import MultipartPostHandler
from urllib import urlencode
from cookielib import CookieJar
from dofler.log import log 
from dofler.common import md5hash

class DoflerClient(object):
    '''
    DoFler API Client Class.  This class handles all client-side API calls to 
    the DoFler service, regardless of the service is remote or local.
    '''
    def __init__(self, host, port, username, password, ssl=False, anon=True):
        self.host = host
        self.port = port
        self.ssl = ssl
        self.anonymize = anon
        self.username = username
        self.jar = CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),
                            MultipartPostHandler.MultipartPostHandler())
        self.login(username, password)


    def call(url, data):
        '''
        This is the core function that calls the API.  all API calls route
        through here.

        :param url: URL of Call
        :param data: Data to be sent with call

        :type url: str 
        :type data: dictionary, str 

        :return: urllib2 Response Object
        '''
        ssl = {
            True: 'https://',
            False: 'http://'
        }
        return self.opener.open('%s%s:%s%s' % (ssl[self.ssl], self.host, 
                                               self.port, url, data))


    def login(self, username, password):
        '''
        Login Function.

        :param username: username/sensorname
        :param password: username/sensorname password

        :type username: str
        :type password: str

        :return: None
        '''
        date = str(time.time())
        data = {
            'timestamp': date,
            'username': username,
            'md5hash': md5hash(username, date, password)
        }
        self.call('/auth/login', urlencode(data))


    def account(self, username, password, info, proto, parser):
        '''
        Account API call.  This function handles adding accounts into the
        database.

        :param username: Account Username
        :param password: Account Password
        :param info: General Information Field
        :param proto: Discovered Protocol
        :param parser: Parser/Agent to discovere account 

        :type username: str 
        :type password: str 
        :type info: str 
        :type proto: str 
        :type parser: str

        :return: None
        '''
        # If the anonymization bit is set, then we need to hide the password. 
        # We will still display the first 3 characters, however will asterisk
        # the rest of the password past that point.
        if self.anonymize:
            if len(password) >= 3:
                password = '%s%s' % (password[:3], '*' * (len(password) - 3))
        self.call('/post/account', urlencode({
            'username': username,
            'password': password,
            'info': info,
            'proto': proto,
            'parser': parser,
        }))


    def image(self, fobj, filename):
        '''
        Image API Call.  Uploads the image into the database.

        :param fobj: File-like object with the image contents
        :param filename: Filename or extension of the file. 

        :type fobj: fileobject
        :type filename: str 

        :return: None
        '''
        try:
            self.call('/post/image', {'file': fobj, 
                'filetype': filename.split('.')[-1]})
        except:
            try:
                log.error('API: Upload Failed. %s=%skb' % (filename, 
                                            os.path.getsize(filename) / 1024)))
            except:
                log.error('API: %s doesnt exist' % filename)


    def stat(self, proto, count):
        '''
        Statistical API call.  Sends the 1 minute count of packets for a given
        protocol to the backend database.

        :param proto: Protocol name
        :param count: Packet count

        :type proto: str 
        :type count: int 

        :return: None
        '''
        self.call('/post/stats', urlencode({'proto': proto, 'count': count, 
                                            'username': self.username}))


    def reset(self, env):
        '''
        Reset API call.  Sends a reset code to the API for the given type of
        data. 

        :param env: Environment Type.  Valid types are: images, accounts
        :type env: str 
        :return: None 
        '''
        self.call('/post/reset/%s' % env, None)