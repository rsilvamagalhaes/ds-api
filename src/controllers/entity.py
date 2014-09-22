from google.appengine.ext import ndb
import datetime
import sys
import logging


def put(json):

    kind = json['kind']
    if 'ancestor' in json:
        json_parent = json['ancestor']
        parent_key = create_key(json_parent)
        p = create_generic_model_with_parent(kind, parent_key)
    else:
        p = create_generic_model(kind)

    for field in json['fields']:
        if 'type' in field:
            value = from_filter_type(field['value'], field['type'])
            setattr(p, field['field'], value)
        else:
            setattr(p, field['field'], field['value'])

    p.put()


def create_generic_model(kind):
    class GenericModel(ndb.Expando):
        @classmethod
        def _get_kind(cls):
            return kind

    return GenericModel()


def create_generic_model_with_parent(kind, parent_key):
    class GenericModel(ndb.Expando):
        @classmethod
        def _get_kind(cls):
            return kind

    return GenericModel(parent=parent_key)


def create_key(json):
    kind = json['kind']
    identifier = __get_identifier_to_key(json)
    return ndb.Key(flat=[kind, identifier])


def __get_identifier_to_key(json):
    identifier = None

    if 'id' in json:
        identifier = json['id']

    if 'name' in json:
        identifier = json['name']

    return identifier


def from_filter_type(value, field_type):
    options = {'date': __long_to_date}
               # 'key': get_key}

    if field_type in options:
        return options[field_type](value)
    else:
        return value


def to_filter_type(value):
    options = {'date': __date_to_long, 'key': __model_to_json}
    field_type = __get_field_type(value)

    if field_type in options:
        return options[field_type](value)
    else:
        return value

def __get_field_type(value):
    if type(value) is datetime.datetime:
        return 'date'
    elif type(value) is ndb.Expando:
        return 'key'
    else:
        return None


def __long_to_date(value):
    return datetime.datetime.fromtimestamp(value/1000)

def __model_to_json(value):
    return value._to_dict()['kind']

def __date_to_long(value):
    return __unix_time_millis(value)


def __unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()


def __unix_time_millis(dt):
    return __unix_time(dt) * 1000.0
