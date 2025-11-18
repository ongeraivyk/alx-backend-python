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
# Task 2 decorator: transactional
# -----------------------------
def transactional(func):
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit changes if successful
            return result
        except Exception as e:
            conn.rollback()  # Rollback if any error occurs
            print(f"[ERROR] Transaction failed: {e}")
            raise  # Re-raise the exception
    return wrapper

# -----------------------------
# Example function
# -----------------------------
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)
    )

# -----------------------------
# Run example
# -----------------------------
try:
    update_user_email(user_id=1, new_email="new_email@example.com")
    print("User email updated successfully.")
except Exception:
    print("Failed to update user email.")
