from google.appengine.ext import ndb
from bottle import Bottle
import sys
bottle = Bottle()


def createGeneric(kind):

   class GenericModel(ndb.Expando):
        @classmethod
        def _get_kind(cls):
            return kind

   return GenericModel()


#[GenericModel(key=Key('User', 5838406743490560), nome='Guilherme', senha='123456'),
#  GenericModel(key=Key('User', 6192449487634432), nome='Guilherme', senha='123456')]
def toJSON(query_result):
    list = []
    for model in query_result:
        item = {}
        for property in model._properties.keys():
            value = getattr(model, property)
            item[property] = value
            
        list.append(item)

    return {'result': list}


@bottle.get('/query/put')
def put():
    json = {
        'kind': 'User',
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

    p = createGeneric(json['kind'])

    for field in json['fields']:
        setattr(p, field['field'], field['value'])

    p.put()

    return 'OK'

@bottle.get('/query/get')
def get():

    json = {
        'kind': 'User',
        'filters': [{
            'field': 'nome',
            'operator': '=',
            'value': 'Guilherme'
        }]
    }


    try:
        user = createGeneric(json['kind'])
        query = user.query()
        for filter in json['filters']:
            query = query.filter(ndb.GenericProperty(filter['field']) == filter['value'])

        return toJSON(query.fetch())

    except:
        print sys.exc_info()

