from google.appengine.ext import ndb
import datetime
import sys
import query

def put(json):
    p = create_generic_model(json['kind'])

    for field in json['fields']:
        if 'type' in field:
            setattr(p, field['field'], from_filter_type(field['value'], field['type']))
        else:
            setattr(p, field['field'], field['value'])

    return p.put().urlsafe()


def create_generic_model(kind):
    class GenericModel(ndb.Expando):
        @classmethod
        def _get_kind(cls):
            return kind

    return GenericModel()


def get_key(json):
    kind = json['kind']
    ancestors = []
    ancestors.append(kind)

    identifier = get_identifier_from_ancestor(json)
    ancestors.append(identifier)

    if 'ancestor' in json:
        ancestors = get_ancestors(json, ancestors)

    key = ndb.Key(flat=ancestors)
    return key


def get_ancestors(json, ancestors):
    while 'ancestor' in json:
        ancestor_kind = json['kind']
        identifier = get_identifier_from_ancestor(json)

        ancestors.append(ancestor_kind)
        ancestors.append(identifier)

        json = json['ancestor']

    return ancestors


def get_identifier_from_ancestor(json):
    identifier = None

    if 'name' in json:
        identifier = json['name']

    if 'id' in json:
        identifier = long(json['id'])

    return identifier


def from_filter_type(value, field_type):
    options = {'date': __long_to_date,
               'key': get_key}

    if field_type in options:
        return options[field_type](value)
    else:
        return value


def to_filter_type(value):
    options = {'date': __date_to_long}
    field_type = __get_field_type(value)

    if field_type in options:
        return options[field_type](value)
    else:
        return value


def __get_field_type(value):
    if type(value) is datetime.datetime:
        return 'date'
    else:
        return None


def __long_to_date(value):
    return datetime.datetime.fromtimestamp(
        int(value)
    )


def __date_to_long(value):
    return __unix_time_millis(value)


def __unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()


def __unix_time_millis(dt):
    return __unix_time(dt) * 1000.0