from google.appengine.ext import ndb
import src.controllers.entity as entity_api

QUERY_LIMIT = 30

def execute(json):
    kind = json['kind']

    if 'key' in json:
        json_result = result_by_key(json)

    elif 'ancestor' in json:
        json_result = __result_by_ancestor(json)

    else:

        entity = entity_api.create_generic_model(kind)
        query = entity.query()

        query = __apply_filters(json, query)
        query = __apply_orders(json, query)

        limit = __set_limit(json)
        fetch = query.fetch(limit)
        json_result = __to_json(fetch)

    return {'result': json_result}


def __set_limit(json):
    limit = QUERY_LIMIT
    if 'limit' in json:
        limit = int(json['limit'])

    return limit


def __to_json(query_result):
    if not isinstance(query_result, list):
        query_result = [query_result]

    result_json = []
    for model in query_result:

        if model != None:
            item = __model_to_json(model)
            result_json.append(item)

    return result_json


def __model_to_json(model):
    json_model = {}

    if model:
        json_model['id'] = model.key.id()
        json_model['kind'] = model.key.kind()
        json_model['fields'] = []

        for prop in model._properties.keys():
            item = {}
            value = getattr(model, prop)
            item['field'] = prop
            item['value'] = entity_api.to_filter_type(value)
            item['type'] = value.__class__.__name__

            json_model['fields'].append(item)

    return json_model


def __result_by_ancestor(json):
    parent_json = json['ancestor']
    ancestor_key = entity_api.create_key(parent_json)

    kind = json['kind']
    query = entity_api.create_generic_model(kind).query(ancestor=ancestor_key)
    return __to_json(query.fetch(QUERY_LIMIT))


def result_by_key(json):
    json_key = json['key']
    key = entity_api.create_key(json_key)
    result_from_db = key.get()

    return __to_json(result_from_db)


def __is_ancestor_json(json):
    return not 'id' in json and not 'name' in json

def __apply_orders(json, query):
    if 'order' in json:
        query = __order_query(json['order'], query)

    return query

def __apply_filters(json, query):
    if 'filters' in json:
        for query_filter in json['filters']:
            query = __do_query_based_on_operator(query_filter, query)

    return query


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
    filter_field = query_filter['field']

    if 'type' in query_filter:
        filter_field_type = query_filter['type']
    else:
        filter_field_type = None

    filter_value = entity_api.from_filter_type(query_filter['value'], filter_field_type)

    operator = query_filter['operator']

    if operator == '=':
        return query.filter(ndb.GenericProperty(filter_field) == filter_value)
    elif operator == 'in':
        return query.filter(ndb.GenericProperty(filter_field).IN(filter_value))
    elif operator == '>':
        return query.filter(ndb.GenericProperty(filter_field) > filter_value)
    elif operator == '>=':
        return query.filter(ndb.GenericProperty(filter_field) >= filter_value)
    elif operator == '<':
        return query.filter(ndb.GenericProperty(filter_field) < filter_value)
    elif operator == '<=':
        return query.filter(ndb.GenericProperty(filter_field) <= filter_value)
