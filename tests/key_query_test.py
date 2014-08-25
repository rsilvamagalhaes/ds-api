import pytest
import src.controllers.entity as entity_api
import src.controllers.query as query_api
from google.appengine.ext import ndb
import json

FATHERS_NAME = "Celso"

entity_json_father = {"kind": "User","fields": [{"field": "nome","value": FATHERS_NAME}]}
entity_json_son    = {"kind": "User","fields": [{"field": "nome","value": "Bob"}, {"type": "key","field": "pai", "value": {"kind":"User", "id": 111}}]}

query_operator_eq_father = {'kind':'User','filters':[{'field':'nome', 'value': FATHERS_NAME, 'operator': '='}]}
query_find_father_by_key_id   = {'kind': 'User', 'key': {'kind': 'User', 'id': 31233132131}}


def test_create_entity_with_key_field():
    entity_api.put(entity_json_father)

    father_json = query_api.execute(query_operator_eq_father)
    assert len(father_json['result']) == 1


def test_get_entity_by_key():
    entity_api.put(entity_json_father)

    father_json = query_api.execute(query_operator_eq_father)
    assert len(father_json['result']) == 1

    change_id_of_son_and_change_query(father_json)
    entity_api.put(entity_json_son)

    son_json = query_api.execute(query_find_father_by_key_id)
    assert len(son_json['result']) == 1
    assert get_father_id(father_json) == son_json['result'][0]['id']
    assert FATHERS_NAME == son_json['result'][0]['fields'][0]['value']


def get_father_id(father_json):
    return father_json['result'][0]['id']

def change_id_of_son_and_change_query(father_json):
    father_id = get_father_id(father_json)
    entity_json_son['fields'][1]['value']['id'] = str(father_id)
    query_find_father_by_key_id['key']['id'] = father_id