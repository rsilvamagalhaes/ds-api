from google.appengine.ext import ndb
import src.controllers.entity as entity_api

QUERY_LIMIT = 30

def execute(json):
    kind = json['kind']

    if 'key' in json or 'ancestor' in json:
        json_result = get_results_from_key(json)

    else:
        entity = entity_api.create_generic_model(kind)
        query = entity.query()

        if 'filters' in json:
            for query_filter in json['filters']:
                query = __do_query_based_on_operator(query_filter, query)

        if 'order' in json:
            query = __order_query(json['order'], query)

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

    result_json = []
    for model in query_result:

        if model != None:
            item = model_to_json(model)
            result_json.append(item)

    return result_json


def __decide_which_key_will_use(json):
    if 'key' in json:
        json = json['key']
    else:
        json = json['ancestor']

    return json


def model_to_json(model):
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


def get_results_from_key(json):
    key = entity_api.get_key(json)
    result_from_db = key.get()

    if not isinstance(result_from_db, list):
        result_from_db = [result_from_db]

    return __to_json(result_from_db)


def get_identifier_from_ancestor(json):
    identifier = None

    if 'name' in json:
        identifier = json['name']

    if 'id' in json:
        identifier = long(json['id'])

    return identifier


def get_ancestors(json, ancestors):
    while 'ancestor' in json:
        ancestor_kind = json['kind']
        identifier = get_identifier_from_ancestor(json)

        ancestors.append(ancestor_kind)
        ancestors.append(identifier)

        json = json['ancestor']

    return ancestors


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
