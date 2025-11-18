import sqlite3
import functools

# -----------------------------
# Task 1: Connection decorator
# -----------------------------
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)  # Pass the connection to the function
            return result
        finally:
            conn.close()  # Ensure connection is closed even if an error occurs
    return wrapper

# -----------------------------
# Example function
# -----------------------------
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# -----------------------------
# Run example
# -----------------------------
user = get_user_by_id(user_id=1)
print(user)
