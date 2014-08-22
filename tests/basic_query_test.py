import pytest
import src.controllers.entity as entity_api
import src.controllers.query as query_api
from google.appengine.ext import ndb
import json

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
        },
        {
            'field': 'idade',
            'value': 21
        }
    ]
}

query_limit = {"kind": "User"}

def test_limit():
    entity_api.put(put_entity_json)

    json = query_api.execute(query_limit)
    assert len(json['result']) == 1

    for i in xrange(0,10):
        entity_api.put(put_entity_json)

    json = query_api.execute(query_limit)
    assert len(json['result']) == 11


def test_max_limit():
    for i in xrange(0, 35):
        entity_api.put(put_entity_json)

    json = query_api.execute(query_limit)
    assert len(json['result']) == 30

