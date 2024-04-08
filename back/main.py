import asyncio
import aioredis
import asyncpg
from fastapi import FastAPI, HTTPException
from database import queries
from database.queries import connect_to_database
from utils import db_query_tool, make_exceptions
from fastapi.middleware.cors import CORSMiddleware

# TODO


# 7. aioredis

# 1. переписать на sanic
# 2. переписать на django
# 7. redis


# 3. Цикл в sql DONE
# 4. Union, -, + PLUS MINUS DONE
# 5. Модальные окна, лодеры DONE
# 6. Разница join'ов DONE


# TODO LEFT JOIN к каждому значению левой таблицы приклеивает значение правой таблицы. Если значения в правой таблице нет, то оставляет null
# '''
# SELECT creation_date, age FROM logs
# LEFT JOIN people ON logs.username = people.firstname
# '''

# TODO INNER JOIN возвращает значения таблиц, которые полностью совпадают
# '''
# SELECT creation_date, age FROM logs
# INNER JOIN people ON logs.username = people.firstname
# '''

# TODO RIGHT JOIN к каждому значению правой таблицы приклеивает значение левой таблицы. Если значения в левой таблице нет, то оставляет null
# '''
# SELECT creation_date, age FROM logs
# RIGHT JOIN people ON logs.username = people.firstname
# '''

# '''
# SELECT id, 1 as priority FROM people
# UNION
# SELECT id, 0 as priority FROM logs
# ORDER BY priority DESC, id ASC
# '''

# '''
# SELECT * FROM (SELECT id, 1 as priority FROM people
# UNION
# SELECT id, 0 as priority FROM logs
# ORDER BY priority DESC, id ASC) AS selected_data
#
# 	EXCEPT
#
# SELECT id, 1 as priority FROM people
# WHERE id % 2 != 0
# ORDER BY priority DESC, id ASC
# '''

# '''
# SELECT DISTINCT id, priority FROM (SELECT * FROM (SELECT id, 1 as priority FROM people
# UNION
# SELECT id, 0 as priority FROM logs
# ORDER BY priority DESC, id ASC) AS selected_data
#
# 	UNION ALL
#
# SELECT id, 1 as priority FROM people
# WHERE id % 2 = 0
# ORDER BY priority DESC, id ASC) AS selected_data_with_union
# ORDER BY priority DESC, id ASC
# '''


# '''
# SELECT * FROM (SELECT * FROM (SELECT id, 1 as priority FROM people
# UNION
# SELECT id, 0 as priority FROM logs
# ORDER BY priority DESC, id ASC) AS selected_data
#
# 	UNION ALL
#
# SELECT id, 1 as priority FROM people
# WHERE id % 2 = 0
# ORDER BY priority DESC, id ASC) AS selected_data_with_union_all
# '''


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    app.state.connection = await queries.connect_to_database()


@app.on_event("shutdown")
async def shutdown():
    await queries.disconnect_from_database(app.state.connection)


@make_exceptions
@app.post('/api/users/')
async def create_user(person: dict):
    await asyncio.sleep(1)
    await db_query_tool('SELECT create_user($1)', 'post', person)
    return {"message": "ok"}


@make_exceptions
@app.get('/api/users/')
async def get_users():
    await asyncio.sleep(1)
    users = await db_query_tool('''
    SELECT pl.id, pl.firstname, pl.fullname, pl.age FROM people as pl
    ORDER BY pl.firstname    
    ''', 'get')
    return {"data": users}


@make_exceptions
@app.put('/api/users/{user_id}')
async def update_user(person: dict, user_id: int):
    await asyncio.sleep(1)
    await db_query_tool(
        'SELECT update_user($1, $2, $3, $4)', 'update',
        *[x for x in person.values()], user_id)

    return {"message": f"User with ID {user_id} updated successfully"}


@make_exceptions
@app.delete('/api/users/{user_id}')
async def delete_user(user_id: int):
    await asyncio.sleep(1)
    await db_query_tool('CALL delete_user_by_id($1)', 'delete', user_id)
    return {"message": f"User with ID {user_id} deleted successfully"}


@make_exceptions
@app.get('/api/dates')
async def get_dates():
    dates = await db_query_tool('''
   SELECT get_dates()
    ''', 'get')
    return {"dates": dates}


@make_exceptions
@app.get('/api/cache')
async def get_cache():
    redis = aioredis.from_url("redis://localhost")
    if redis.exists("my-key"):
        return {'message': 'Cache exists'}

    await redis.set("my-key", "value")
    value = await redis.get("my-key")
    return {'data': value}













