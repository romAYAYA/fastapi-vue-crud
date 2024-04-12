from sanic import Sanic, response, json, file
from sanic_ext import Extend
import redis
from database import queries
from utils import make_exceptions, db_query_tool

redis_client = redis.Redis(host='localhost', port=6379, db=0)

app = Sanic('privet')

app.static('/assets', './static/dist/assets')

app.config.CORS_ORIGINS = "http://localhost:5173"
Extend(app)


@app.listener("before_server_start")
async def startup(app, loop):
    app.state.connection = await queries.connect_to_database()


@app.listener("after_server_stop")
async def shutdown(app, loop):
    await queries.disconnect_from_database(app.state.connection)


@app.route("/")
async def handler(request):
    return await file('static/dist/index.html')


@make_exceptions
@app.get('/api/users/')
async def get_users(request):
    users = await db_query_tool('''
    SELECT pl.id, pl.firstname, pl.fullname, pl.age FROM people as pl
    ORDER BY pl.firstname    
    ''', 'get')
    serialized_users = []
    for user in users:
        serialized_user = {
            "id": user[0],
            "firstname": user[1],
            "fullname": user[2],
            "age": user[3]
        }
        serialized_users.append(serialized_user)

    return json({"data": serialized_users})


@make_exceptions
@app.put('/api/users/<user_id:int>/')
async def update_user(request, user_id: int):
    person = request.json

    await db_query_tool('''
        SELECT update_user($1, $2, $3, $4)
    ''', 'update', *list(person.values()), user_id)

    return response.json({"message": f"User with ID {user_id} updated successfully"})


@make_exceptions
@app.delete('/api/users/<user_id:int>')
async def delete_user(request, user_id: int):
    await db_query_tool('CALL delete_user_by_id($1)', 'delete', user_id)
    return response.json({"message": f"User with ID {user_id} deleted successfully"})


@make_exceptions
@app.post('/api/users/')
async def create_user(request):
    person = request.json
    await db_query_tool('SELECT create_user($1)', 'post', person)
    return response.json({"message": "ok"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
