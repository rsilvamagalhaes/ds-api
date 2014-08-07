from google.appengine.ext import ndb
import entity as entity_api
from bottle import Bottle
bottle = Bottle()


def execute(json):
    kind = json['kind']

    #Key methods
    if 'name' in json or 'id' in json:
        json_result = get_results_from_key(kind, json)

    else:
        entity = entity_api.create_generic_model(kind)
        query = entity.query()

        if 'filters' in json:
            for query_filter in json['filters']:
                query = __do_query_based_on_operator(query_filter, query)

        if 'order' in json:
            query = __order_query(json['order'], query)

        limit = None
        if 'limit' in json:
            limit = int(json['limit'])

        fetch = query.fetch(limit)
        json_result = __to_json(fetch)

    return {'result': [json_result]}


def __to_json(query_result):
    result_json = []

    for model in query_result:
        item = {}
        for prop in model._properties.keys():
            value = getattr(model, prop)
            item[prop] = value

        result_json.append(item)

    return result_json


def model_to_json(model):
    item = {}
    if model:
        for prop in model._properties.keys():
            value = getattr(model, prop)
            item['field'] = prop
            item['value'] = value
            item['type'] = value.__class__.__name__
    return item


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


def __order_query(order_json, query):
    for order in order_json:
        order_direction = order['direction']
        order_field = order['field']

        if order_direction == 'ASC':
            query = query.order(ndb.GenericProperty(order_field))
        else:
            query = query.order(-ndb.GenericProperty(order_field))

    return query


def __do_query_based_on_operator(query_filter, query):
    if query_filter['operator'] == '=':
        return query.filter(ndb.GenericProperty(query_filter['field']) == query_filter['value'])
    elif query_filter['operator'] == '>':
        return query.filter(ndb.GenericProperty(query_filter['field']) > query_filter['value'])
    elif query_filter['operator'] == 'in':
        return query.filter(ndb.GenericProperty(query_filter['field']).IN(query_filter['value']))