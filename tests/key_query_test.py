import pytest
import src.controllers.entity as entity_api
import src.controllers.query as query_api

FATHERS_NAME = "Celso"
SONS_NAME = "Bob"

entity_father = {"kind": "User","fields": [{"field": "nome","value": FATHERS_NAME}]}
entity_son    = {"kind": "User","fields": [{"field": "nome","value": SONS_NAME}, {"type": "key","field": "pai", "value": {"kind":"User", "id": 111}}]}

query_operator_eq_father = {'kind':'User','filters':[{'field':'nome', 'value': FATHERS_NAME, 'operator': '='}]}
query_find_father_by_key_id   = {'kind': 'User', 'key': {'kind': 'User', 'id': 111}}


def test_create_entity_with_key_field():
    entity_api.put(entity_father)
    father_json = query_api.execute(query_operator_eq_father)
    assert len(father_json['result']) == 1


def test_get_entity_by_key():
    entity_api.put(entity_father)

    father_json = query_api.execute(query_operator_eq_father)
    assert len(father_json['result']) == 1

    change_id_of_son_and_change_query(father_json, entity_son)
    entity_api.put(entity_son)

    son_json = query_api.execute(query_find_father_by_key_id)
    assert len(son_json['result']) == 1
    assert get_father_id(father_json) == son_json['result'][0]['id']
    assert FATHERS_NAME == son_json['result'][0]['fields'][0]['value']


entity_son_ancestor  = {"kind": "User","fields": [{"field": "nome","value": SONS_NAME}], "ancestor": {"kind":"User", "id": 111}}
query_find_son_by_ancestor = {"kind": "User", "ancestor": {"kind": "User", "id": 111}}

def test_put_ancestor():
    entity_api.put(entity_father)

    father = query_api.execute(query_operator_eq_father)
    assert len(father['result']) == 1

    father_id = get_father_id(father)
    entity_son_ancestor['ancestor']['id'] = father_id
    entity_api.put(entity_son_ancestor)

    # query_operator_eq_son = {'kind':'User','filters':[{'field':'nome', 'value': SONS_NAME, 'operator': '='}]}
    # print query_api.execute(query_operator_eq_son)
    # print query_api.execute(query_find_son_by_ancestor)

    query_find_son_by_ancestor['ancestor']['id'] = father_id
    result_by_ancestor = query_api.execute(query_find_son_by_ancestor)
    assert len(result_by_ancestor['result']) == 1

    name_of_son = result_by_ancestor['result'][0]['fields'][0]['value']
    assert name_of_son == SONS_NAME
    assert father_id == result_by_ancestor['result'][0]['id']


def get_father_id(father_json):
    return father_json['result'][0]['id']

def change_id_of_son_and_change_query(father_json, son_json):
    father_id = get_father_id(father_json)
    change_son_id(entity_son, father_id)
    query_find_father_by_key_id['key']['id'] = father_id

def change_son_id(son, father_id):
    son['fields'][1]['value']['id'] = str(father_id)