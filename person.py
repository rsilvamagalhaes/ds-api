from google.appengine.ext import ndb
from bottle import Bottle
bottle = Bottle()


class GenericModel(ndb.Expando):

    @classmethod
    def _get_kind(cls):
        return 'Entidade'


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

    p = GenericModel()
    p.kind = 'User'

    for field in json['fields']:
        setattr(p, field['field'], field['value'])

    p.put()

    return 'OK'

