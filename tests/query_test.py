import pytest
import entity as entity_api
import query as query_api
from google.appengine.ext import ndb

def create_generic_model(kind):
    class GenericModel(ndb.Expando):
        @classmethod
        def _get_kind(cls):
            return kind

    return GenericModel()


put_entity_json = {
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

query_json = {'kind': 'User', 'filters': [{'field': 'nome', 'operator': '=', 'value': 'Luana Silva'}]}

def test_basic_query_with_filter_operator_eq():
    entity_api.put(put_entity_json)

    user_entity = create_generic_model('User')
    print query_api.execute()

