import sqlite3
import functools
from datetime import datetime

# Decorator to log SQL queries with timestamp and function name
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the SQL query from positional or keyword arguments
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] [LOG] Function '{func.__name__}' executing SQL Query: {query}")
        else:
            print(f"[LOG] Function '{func.__name__}' called, but no SQL query found.")
        # Execute the original function
        return func(*args, **kwargs)
    return wrapper

# Example usage
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
