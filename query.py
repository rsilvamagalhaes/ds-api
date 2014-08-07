from google.appengine.ext import ndb
import entity as entity_api


def execute(json):
    entity = entity_api.create_generic_model(json['kind'])
    query = entity.query()

    if 'filters' in json:
        for query_filter in json['filters']:
            query = __do_query_based_on_operator(query_filter, query)

    if 'order' in json:
        query = __order_query(json['order'], query)

    fetch = query.fetch()
    return __to_json(fetch)


def __to_json(query_result):
    result_json = []

    for model in query_result:
        item = {}
        for prop in model._properties.keys():
            value = getattr(model, prop)
            item[prop] = value

        result_json.append(item)

    return {'result': result_json}


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