import sqlite3
import functools

# -----------------------------
# Task 0: Logging decorator
# -----------------------------
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            print(f"[LOG] Executing SQL query: {query}")
        return func(*args, **kwargs)
    return wrapper

# -----------------------------
# Example function
# -----------------------------
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# -----------------------------
# Run example
# -----------------------------
# Make sure the 'users' table exists in your 'users.db'
users = fetch_all_users(query="SELECT * FROM users")
print(users)
