import pytest
import entity as entity_api
from google.appengine.ext import ndb

def create_generic_model(kind):
    class GenericModel(ndb.Expando):
        @classmethod
        def _get_kind(cls):
            return kind

    return GenericModel()

json = {
    "kind": "User",
    "fields": [
        {
            "field": "nome",
            "value": "Luana Silva"
        },
        {
            "field": "senha",
            "value": "123456"
        }
    ]
}

def test_create_entity():
    entity_api.put(json)

    entity = create_generic_model('User')
    query = entity.query()
    assert len(query.fetch()) == 1

