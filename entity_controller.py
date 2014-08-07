from bottle import Bottle, request, error
import entity as entity_api
bottle = Bottle()


@error(404)
def error404():
    return 'Nothing here, sorry'


@bottle.post('/api/entity')
def put():
    inserted_key = entity_api.put(request.json)
    return inserted_key