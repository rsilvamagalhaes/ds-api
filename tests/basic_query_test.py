import pytest
import src.controllers.entity as entity_api
import src.controllers.query as query_api
from google.appengine.ext import ndb
import json

put_entity_json = {"kind": "User","fields": [{"field": "nome","value": "Luana Silva"},{"field": "senha","value": "123456"},{'field': 'idade','value': 21}]}
query_limit = {"kind": "User"}

def get_fields(json):
    if 'fields' in json:
        return json['fields']
    else:
        return []


def test_limit():
    for i in xrange(0,10):
        entity_api.put(put_entity_json)

    json = query_api.execute(query_limit)
    assert len(json['result']) == 10


def test_max_limit():
    for i in xrange(0, 35):
        entity_api.put(put_entity_json)

    json = query_api.execute(query_limit)
    assert len(json['result']) == 30


query_fields = {"kind":"User", "fields":["nome", "senha"]}
def test_projection_query():
    entity_api.put(put_entity_json)

    json = query_api.execute(query_fields)
    assert len(json['result'][0]['fields']) == 2

def put_user_changing_ages():
    for i in xrange(0, 3):
        put_entity_json['fields'][2]['value'] = 21 + i
        entity_api.put(put_entity_json)


query_desc = {"kind": "User","order": [{"field": "idade","direction": "DESC"}]}

def test_query_order_desc():
    put_user_changing_ages()

    json = query_api.execute(query_desc)
    ages = [23,22,21]
    for index, entity in enumerate(get_fields(json)):
        for field in entity:
            if 'idade' in field['field']:
                assert ages[index] == field['value']


query_asc = {"kind": "User","order": [{"field": "idade","direction": "ASC"}]}

def test_query_order_asc():
    put_user_changing_ages()

    json = query_api.execute(query_asc)
    ages = [21,22,23]
    for index, entity in enumerate(get_fields(json)):
        for field in entity:
            if 'idade' in field['field']:
                assert ages[index] == field['value']


query_asc_and_desc = {"kind": "User","order": [{"field": "nome","direction": "ASC"},{"field": "idade","direction": "DESC"}]}
query_asc_and_desc_2 = {"kind": "User", "order": [{"field": "idade","direction": "ASC"},{"field": "nome","direction": "DESC"}]}

def test_query_order_desc_and_asc():
    names = ['Felipe Volpone','Gustavo Silverio','Guilherme Gotardo']
    for i in xrange(0, 3):
        put_entity_json['fields'][1]['value'] = names[i]
        entity_api.put(put_entity_json)

    json = query_api.execute(query_asc_and_desc_2)
    for index, entity in enumerate(get_fields(json)):
        for field in entity:
            if 'name' in field['field']:
                assert names[index] == field['value']

















