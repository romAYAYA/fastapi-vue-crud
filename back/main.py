import asyncpg
from fastapi import FastAPI, HTTPException
from database import queries
from database.queries import connect_to_database
from utils import db_query_tool, make_exceptions
from fastapi.middleware.cors import CORSMiddleware


# TODO
# 1. переписать на sanic
# 2. переписать на django


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
    await db_query_tool('SELECT create_user($1)', 'post', person)
    return {"message": "ok"}


@make_exceptions
@app.get('/api/users/')
async def get_users():
    users = await db_query_tool('''
    SELECT pl.id, pl.firstname, pl.fullname, pl.age FROM people as pl
    ORDER BY pl.firstname    
    ''', 'get')
    return {"data": users}


@make_exceptions
@app.put('/api/users/{user_id}')
async def update_user(person: dict, user_id: int):
    print('\n\n\n\n\n\n\n', person)
    print('\n\n\n\n\n\n\n', user_id)
    await db_query_tool(
        'SELECT update_user($1, $2, $3, $4)', 'update',
        *[x for x in person.values()], user_id)

    return {"message": f"User with ID {user_id} updated successfully"}


@make_exceptions
@app.delete('/api/users/{user_id}')
async def delete_user(user_id: int):
    await db_query_tool('CALL delete_user_by_id($1)', 'delete', user_id)
    return {"message": f"User with ID {user_id} deleted successfully"}
