from google.appengine.ext import ndb


def put(json):
    p = create_generic_model(json['kind'])

    for field in json['fields']:
        setattr(p, field['field'], field['value'])

    return p.put().urlsafe()


def create_generic_model(kind):
    class GenericModel(ndb.Expando):
        @classmethod
        def _get_kind(cls):
            return kind

    return GenericModel()