from bottle import Bottle, template
from google.appengine.ext import ndb
import sys

bottle = Bottle()

@bottle.error(404)
def error_404(error):
    return 'Sorry, nothing at this URL.'

@bottle.get('/adm')
def adm():
    return template('src/templates/adm.html')
