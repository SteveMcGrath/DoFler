from hashlib import md5
import logging
import json
from md5 import md5hash
from dofler.models import Setting, User
from dofler.db import Session, SettingSession


_loglevels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}
_log_to_console = False
_log_to_file = False
log = logging.getLogger('DoFler')
#sqllog = logging.getLogger('sqlalchemy.engine')
#sqllog.setLevel(logging.INFO)
#hdlr = logging.FileHandler('/var/log/dofler-sql.log')
#hdlr.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
#sqllog.addHandler(hdlr)

def log_to_console():
    '''
    Enables Console logging if not already enabled. 
    '''
    global _log_to_console
    if not _log_to_console and setting('log_console').boolvalue:
        stderr = logging.StreamHandler()
        console_format = logging.Formatter('%(levelname)s %(message)s')
        stderr.setFormatter(console_format)
        log.setLevel(_loglevels[setting('log_console_level').value])
        log.addHandler(stderr)
        _log_to_console = True


def log_to_file():
    '''
    Enables logging output to a file if not already enabled. 
    '''
    global _log_to_file
    if not _log_to_file and setting('log_file').boolvalue:
        hdlr = logging.FileHandler(setting('log_file_path').value)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        hdlr.setFormatter(formatter)
        log.setLevel(_loglevels[setting('log_file_level').value])
        log.addHandler(hdlr)
        _log_to_file = True


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


def jsonify(data):
    '''
    A simple shortcut for dumping json dictionaries.  This can come in handy
    if we need to make some global settings for how to return json data.

    :param data: Python dictionary dataset. 
    :type data: dict
    :return: str
    '''
    return json.dumps(data, encoding='ISO-8859-1')


def auth(request):
    '''
    Authentication Check.  Returns True or False based on if the account 
    cookie is set.

    :prarm request: The request object for the given page. 
    :prarm db: The SQLAlchemy session object from the page. 

    :type request: request object
    :type db: Session object

    :return: bool    
    '''
    s = SettingSession()
    name = request.get_cookie('user', secret=setting('cookie_key').value)
    try:
        sensor = s.query(User).filter_by(name=name).one()
        value = True
    except:
        value = False
    s.close()
    return value


def auth_login(request):
    '''
    Base Login Function.  This function is what will handle all of the
    authentication for the API and the UI.  While both behave differently as 
    they are different interfaces into the data, they both handle authentication
    the same way.

    :prarm request: The request object for the given page. 
    :prarm db: The SQLAlchemy session object from the page. 

    :type request: request object
    :type db: Session object

    :return: bool
    '''
    s = SettingSession()
    loggedin = False
    if not auth(request):
        username = request.forms.get('username')
        password = request.forms.get('password')
        #try:
        user = s.query(User).filter_by(name=username).one()
        #except:
        #    pass
        #else:
        if user.check(password):
            loggedin = True
    s.close()
    return loggedin


def setting(name):
    '''
    Retreives the specified setting object from the database.  By abstracting
    this out, we can save a lot of menotinous code.

    :param name: Setting name
    :param s: Session object

    :type name: str 
    :type s: Session Object 

    :return: Setting Object
    '''
    s = SettingSession()
    item = s.query(Setting).filter_by(name=name).one()
    s.close()
    return item