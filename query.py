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


def toJSON(query_result):
    list = []
    for model in query_result:
        item = model_to_json(model)
        list.append(item)

    return list


def model_to_json(model):
    item = {}
    if model:
        for property in model._properties.keys():
            value = getattr(model, property)
            item['field'] = property
            item['value'] = value
            item['type'] = value.__class__.__name__
    return item

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
            'field': 'senha',
            'operator': '=',
            'value': '123456'
        }],
        'order' : {
            'direction': 'DESC',
            'fields' : ['nome']
        },
        'limit': 1
    }

    json = {
        'kind': 'User',
        'id': 4785074604081152,
         'ancestor' : {'kind': 'ParentEntity', 'id': 15}
    }

    kind = json['kind']
    user = create_generic_model(kind)

    #key methods
    if 'name' in json or 'id' in json:
        json_result = get_results_from_key(kind, json)

    else:
        #query methods
        query = user.query()

        if 'filters' in json:
            for filter in json['filters']:
                query = do_query_based_on_operator(filter, query)

        if 'order' in json:
            query = order_query(json['order'], query)

        limit = None
        if 'limit' in json:
            limit = int(json['limit'])

        json_result = toJSON(query.fetch(limit))

    return {'result': [json_result]}


#{kind: 'Entity', name: 'someName', ancestor : {kind: 'ParentEntity', id: 15}}
def get_results_from_key(kind, json):
    if 'name' in json:
        identifier = json['name']

    if 'id' in json:
        identifier = json['id']

    key = ndb.Key(kind, identifier)

    if 'ancestor' in json:
        ancestor_kind = json['ancestor']['kind']
        ancestor_id = json['ancestor']['id']
        key = ndb.Key(kind, identifier, ancestor_kind, ancestor_id)

    return model_to_json(key.get())


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


























