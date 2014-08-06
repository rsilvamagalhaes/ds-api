from google.appengine.ext import db

class User(db.Model):
    name = db.StringProperty()
    age = db.IntegerProperty()
