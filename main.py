from bottle import Bottle
import lib.execjs as execjs

bottle = Bottle()

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@bottle.get('/runjs')
def hello():
    ctx = execjs.compile("""
     function add(x, y) {
         return x + y;
     }
    """)
    ctx.call('add',1, 2)


@bottle.error(404)
def error_404(error):
    return 'Sorry, nothing at this URL.'
