from functools import wraps

from database.queries import connect_to_database


async def db_query_tool(query, method, *args):
    res = None
    connection = await connect_to_database()
    if method == 'get':
        res = await connection.fetch(query)
    else:
        print('\n\n\n\n\n\n\n\n', *args)
        await connection.execute(query, *args)
    await connection.close()
    return res


def make_exceptions(func):
    @wraps
    def wrapper(*args, **kwargs):
        try:
            original_result = func(*args, **kwargs)
            return original_result
        except Exception as e:
            return f'smth went wrong: {e}'

    return wrapper
