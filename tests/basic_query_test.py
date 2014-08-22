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


query_desc = {"kind": "User","order": [{"field": "idade","direction": "DESC"}]}

def test_query_order_desc():
    for i in xrange(0, 3):
        put_entity_json['fields'][2]['value'] = 21 + i
        entity_api.put(put_entity_json)

    json = query_api.execute(query_desc)
    ages = [23,22,21]
    for index, entity in enumerate(json['result']):
        for field in entity:
                if 'idade' in field['field']:
                    assert ages[index] == field['value']


query_asc = {"kind": "User","order": [{"field": "idade","direction": "ASC"}]}

def test_query_order_asc():
    for i in xrange(0, 3):
        put_entity_json['fields'][2]['value'] = 21 + i
        entity_api.put(put_entity_json)

    json = query_api.execute(query_asc)
    ages = [21,22,23]
    for index, entity in enumerate(json['result']):
        for field in entity:
                if 'idade' in field['field']:
                    assert ages[index] == field['value']





















