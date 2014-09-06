import pytest
import src.controllers.entity as entity_api
import src.controllers.query as query_api

some_dates = [1417658400000, 1403665200000, 1393902000000]
some_names = ['pedro','zeca','jose']

entity = {"kind": "User","fields": [{"field": "nome","value": "Pedro"},{"field": "ultimoAcesso","value": 1393902000000, "type": "date"}]}
search_date = {"kind": "User", "filters": [{"field": "ultimoAcesso", "operator": "=", "value": 1393902000000, "type": "date"}]}

def test_date_type():
    for i in xrange(0, len(some_dates)):
        change_name(i)
        change_date(i)

        entity_api.put(entity)

    result = query_api.execute(search_date)
    assert 1 == len(result['result'])

    for fields in result['result'][0]['fields']:
        if fields['field'] == 'nome':
            assert "jose" == fields['value']


def change_name(index):
    entity['fields'][0]['value'] = some_names[index]

def change_date(index):
    entity['fields'][1]['value'] = some_dates[index]
