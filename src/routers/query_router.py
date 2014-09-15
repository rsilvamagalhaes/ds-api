from bottle import Bottle, request, error
import sys
from src.controllers import query as query_api

bottle = Bottle()


@error(404)
def error404():
    return 'Nothing here, sorry'


@bottle.post('/api/query')
def do_query():
    result_json = query_api.execute(request.json)
    return result_json
