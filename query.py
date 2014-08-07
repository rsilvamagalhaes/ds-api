from google.appengine.ext import ndb
from bottle import Bottle
import sys
bottle = Bottle()


def create_generic_model(kind):

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
                'value': 'Zaratrusta'
            },
            {
                'field': 'senha',
                'value': '9999'
            }
        ]
    }

    p = create_generic_model(json['kind'])

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
        }],
        'order' : {
            'direction': 'DESC',
            'fields' : ['nome']
        }
    }


    user = create_generic_model(json['kind'])
    query = user.query()
    for filter in json['filters']:
        query = do_query_based_on_operator(filter, query)


    if json['order']:
        query = order_query(json['order'], query)

    return toJSON(query.fetch())


def order_query(order_json, query):
    direction =  order_json['direction']
    for field in order_json['fields']:
        if direction == 'ASC':
            query = query.order(ndb.GenericProperty(field))
        else:
            query = query.order(-ndb.GenericProperty(field))

    return query

def do_query_based_on_operator(filter ,query):
    if filter['operator'] == '=':
        return query.filter(ndb.GenericProperty(filter['field']) == filter['value'])
    else:
        if filter['operator'] == '>':
            return query.filter(ndb.GenericProperty(filter['field']) > filter['value'])


























