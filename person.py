from google.appengine.ext import ndb
from bottle import Bottle
bottle = Bottle()


def createGeneric(kind):

   class GenericModel(ndb.Expando):
        @classmethod
        def _get_kind(cls):
            return kind

   return GenericModel()


@bottle.get('/person/dyn')
def dynamic():
    json = {
        'kind': 'Entity',
        'fields': [
            {
                'field': 'nome',
                'value': 'Guilherme'
            },
            {
                'field': 'senha',
                'value': '123456'
            }
        ]
    }

    p = createGeneric('User')

    for field in json['fields']:
        setattr(p, field['field'], field['value'])

    p.put()

    return 'OK'

