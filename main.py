from bottle import Bottle
from lib.pyv8 import PyV8
bottle = Bottle()

# Note: We don't need to call run() since our application is embedded within
# the App Engine WSGI application server.


@bottle.get('/runjs')
def hello():
    ctxt = PyV8.JSContext()
    ctxt.enter()
    return 'resultado: ' + str(ctxt.eval('1+1'))

@bottle.error(404)
def error_404(error):
    return 'Sorry, nothing at this URL.'
