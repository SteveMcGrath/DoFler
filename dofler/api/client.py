import urllib2
import time
import os
import json
from requests_futures.sessions import FuturesSession
from dofler.common import md5hash, log

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
        self.opener = FuturesSession(max_workers=10)
        self.login(username, password)


    def call(self, url, data, files={}):
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
        location = '%s%s:%s%s' % (ssl[self.ssl], self.host, self.port, url)
        log.debug('CLIENT: %s' % location)
        return self.opener.post(location, data=data, files=files)


    def login(self, username, password):
        '''
        Login Function.

        :param username: username/sensorname
        :param password: username/sensorname password

        :type username: str
        :type password: str

        :return: None
        '''
        self.call('/post/login', {
            'username': username,
            'password': password
        }).result()


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
        self.call('/post/account', {
            'username': username,
            'password': password,
            'info': info,
            'proto': proto,
            'parser': parser,
        })


    def image(self, filename):
        '''
        Image API Call.  Uploads the image into the database.

        :param fobj: File-like object with the image contents
        :param filename: Filename or extension of the file. 

        :type fobj: fileobject
        :type filename: str 

        :return: None
        '''
        if os.path.exists(filename):
            #try:
                self.call('/post/image', {'filetype': filename.split('.')[-1]},
                                         {'file': open(filename, 'rb')})
            #except:
            #    log.error('API: Upload Failed. %s=%skb' % (filename, 
            #                                os.path.getsize(filename) / 1024))
        else:
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
        self.call('/post/stat', {
            'proto': proto, 
            'count': count, 
            'username': self.username
        })


    def reset(self, env):
        '''
        Reset API call.  Sends a reset code to the API for the given type of
        data. 

        :param env: Environment Type.  Valid types are: images, accounts
        :type env: str 
        :return: None 
        '''
        self.call('/post/reset', {'type': env})


    def services(self):
        '''
        Gets the current service statuses. 
        '''
        return json.loads(self.call('/post/services', {
                'action': 'none',
                'parser': 'none',
        }).result().content)


    def start(self, name):
        '''
        Starts the defined service. 
        '''
        return json.loads(self.call('/post/services', {
                'action': 'Start', 
                'parser': name
        }).result().content)


    def stop(self, name):
        '''
        Stops the defined service. 
        '''
        return json.loads(self.call('/post/services', {
            'action': 'Stop', 
            'parser': name
        }).result().content)
