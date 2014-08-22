import pytest
import src.controllers.entity as entity_api
import src.controllers.query as query_api
from google.appengine.ext import ndb
import json

entity_json_father = {"kind": "User","fields": [{"field": "nome","value": "Celso"}]}
entity_json_son = {"kind": "User","fields": [{"field": "nome","value": "Bob"},{'type': 'key','field': 'pai','value': 111}]}

query_operator_eq = {'kind':'User','filters':[{'field':'nome', 'value': 'Celso', 'operator': '='}]}

query_ancestor = {'kind': 'User', 'ancestor': {'kind': 'User', 'id': 15}}
query_key_name = {'kind': 'User', 'key': {'kind': 'User', 'name': 'someName'}}
query_key_id   = {'kind': 'User', 'key': {'kind': 'Entity', 'id': 31233132131}}

def test_create_entity():
    entity_api.put(entity_json_father)
    #entity_api.put(entity_json_son)

    father_json = query_api.execute(query_operator_eq)
    father_id = father_json['result'][0]['id']

    assert len(father_json['result']) == 1

    change_id_of_son_and_change_query(father_id)

    son = query_api.execute()

def change_id_of_son_and_change_query(father_id):
    entity_json_son['fields'][2]['value'] = father_id
    query_key_id['key']['oid']