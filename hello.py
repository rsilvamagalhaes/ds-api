from bottle import Bottle
bottle = Bottle()


@bottle.get('/h/hello')
def hello():
    return 'ola'