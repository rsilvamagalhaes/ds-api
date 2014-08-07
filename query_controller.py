from bottle import Bottle, request, error
import query as query_entity
bottle = Bottle()


@error(404)
def error404():
    return 'Nothing here, sorry'


@bottle.post('/api/query')
def do_query():
    result_json = query_entity.execute(request.json)
    return result_json