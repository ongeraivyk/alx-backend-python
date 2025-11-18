import sqlite3
import functools

# -----------------------------
# Task 1 decorator: handles DB connection
# -----------------------------
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

# -----------------------------
# Task 4 decorator: cache query results
# -----------------------------
query_cache = {}

def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        if query in query_cache:
            print("[CACHE] Returning cached result")
            return query_cache[query]
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        print("[CACHE] Caching result")
        return result
    return wrapper

# -----------------------------
# Example function
# -----------------------------
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# -----------------------------
# Run example
# -----------------------------
# First call: caches the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call: retrieves from cache
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)
