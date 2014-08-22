import pytest
import src.controllers.entity as entity_api
import src.controllers.query as query_api
from google.appengine.ext import ndb
import json

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
        },
        {
            'field': 'idade',
            'value': 21
        }
    ]
}

query_eq = {'kind': 'User', 'filters': [{'field': 'nome', 'operator': '=', 'value': 'Luana Silva'}]}
query_gt = {'kind': 'User', 'filters': [{'field': 'idade', 'operator': '>', 'value': '20'}]}
query_lt = {'kind': 'User', 'filters': [{'field': 'idade', 'operator': '<', 'value': '25'}]}
query_in = {"kind": "User", "filters": [{"field": "nome", "operator": "in", "value": ["Roberto","Bob", "Luana Silva"]}]}

query_eq_no_result = {'kind': 'User', 'filters': [{'field': 'nome', 'operator': '=', 'value': 'Roberto'}]}
query_gt_no_result = {'kind': 'User', 'filters': [{'field': 'idade', 'operator': '>', 'value': '20'}]}
query_lt_no_result = {'kind': 'User', 'filters': [{'field': 'idade', 'operator': '>', 'value': '21'}]}
query_in_no_result = {"kind": "User", "filters": [{"field": "nome", "operator": "in", "value": ["Roberto","Bob"]}]}

def get_fields(json):
    if 'fields' in json:
        return json['fields']
    else:
        return []

def test_basic_query_with_filter_operator_eq():
    entity_api.put(put_entity_json)

    json = query_api.execute(query_eq)
    for fields in get_fields(json):
        for field in fields:

            if 'nome' in field:
                assert field['nome'] == 'Luana Silva'

    json = query_api.execute(query_eq_no_result)
    assert len(json['result']) == 0


def test_basic_query_with_filter_operator_gt():
    entity_api.put(put_entity_json)

    json = query_api.execute(query_gt)
    for fields in get_fields(json):
        for field in fields:

            if 'idade' in field:
                assert field['field'] == '21'


    json = query_api.execute(query_gt_no_result)
    assert len(json['result']) == 0


def test_basic_query_with_filter_operator_lt():
    entity_api.put(put_entity_json)

    json = query_api.execute(query_lt)
    for fields in get_fields(json):
        for field in fields:

            if 'idade' in field:
                assert field['field'] == '21'

    json = query_api.execute(query_lt_no_result)
    assert len(json['result']) == 0


def test_basic_query_with_filter_operator_in():
    entity_api.put(put_entity_json)

    json = query_api.execute(query_in)
    for fields in get_fields(json):
        for field in fields:

            if 'nome' in field:
                assert field['field'] == 'Luana Silva'

    json = query_api.execute(query_in_no_result)
    assert len(json['result']) == 0