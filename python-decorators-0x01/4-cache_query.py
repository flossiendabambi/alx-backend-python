import time
import sqlite3
import functools

# ✅ Simulated global cache (in-memory)
query_cache = {}

# ✅ Decorator to manage DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# ✅ Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)

        if query in query_cache:
            print("[CACHE HIT] Returning cached result.")
            return query_cache[query]
        
        print("[CACHE MISS] Executing and caching query.")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result

    return wrapper

# ✅ Function that uses both decorators
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# ✅ First call — query is executed and cached
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# ✅ Second call — uses cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
