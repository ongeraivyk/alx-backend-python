import sqlite3

class DatabaseConnection:
    """Class-based context manager for SQLite database connections."""

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        return self.cursor  # This is what 'with ... as' will receive

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()  # Rollback on exception
        else:
            self.conn.commit()    # Commit if no exception
        self.conn.close()


# Example usage
if __name__ == "__main__":
    with DatabaseConnection('users.db') as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
