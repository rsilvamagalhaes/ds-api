import sys, os, unittest
from google.appengine.ext import db
from src.models.models import User


class SimpleQueryTest(unittest.TestCase):

    json = {"kind":"User"}

    def test_kind(self):
        u = User()
        u.name = 'ola'
        u.age
        u.put()
        user = User.query(User.name == 'ola')
        self.assertEqual(user.name, u.name)
        #kind = self.json['kind']
        #k = db.Key.from_path(kind)
        #print kind

if __name__ == '__main__':
    unittest.main()
