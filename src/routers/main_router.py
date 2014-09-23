from bottle import Bottle, template
from google.appengine.api import users
import logging

bottle = Bottle()

@bottle.get('/consoleadm')
def adm():
    logging.info('Usuario eh admin: ' + str(users.is_current_user_admin()))
    if users.get_current_user():
        logging.info('Email: ' + users.get_current_user().email())
    return template('src/templates/adm.html')
