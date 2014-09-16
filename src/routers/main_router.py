from bottle import Bottle, template
from google.appengine.ext import ndb
from google.appengine.api import users
import sys, logging

bottle = Bottle()

@bottle.error(404)
def error_404(error):
    return 'Sorry, nothing at this URL.'

@bottle.get('/adm')
def adm():
    logging.info('Usuario eh admin: ' + str(users.is_current_user_admin()))
    return template('src/templates/adm.html')
