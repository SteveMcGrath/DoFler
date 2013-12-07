from dofler.config import config
from bottle import Bottle, request, response, redirect, static_file, error
from hashlib import md5
from dofler.common import md5hash, auth, auth_login, setting

app = Bottle()

@app.post('/login')
def login():
    '''Login function'''
    if auth_login(request):
        response.set_cookie('user', 
            request.forms.get('username'), 
            secret=setting('cookie_key').value,
            path='/'
        )
        response.add_header('Authentication', 'SUCCESS')
    else:
        response.add_header('Authentication', 'FAILURE')


@app.get('/logout')
def logout():
    '''Simply deletes the account cookie, effectively logging the sensor out.'''
    response.delete_cookie('user',
        request.get_cookie('user', secret=setting('cookie_key').value),
        secret=setting('cookie_key').value)
    )