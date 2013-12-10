import post
import view
import client
import ui
from bottle import Bottle, redirect

app = Bottle()
app.mount('/post', post.app)
app.mount('/get', view.app)
app.mount('/ui', ui.app)

@app.get('/')
def redirect_home():
    redirect('/ui')