import sqlite3


class ExecuteQuery:
    def __init__(self, db_file, query, params=()):
        self.db_file = db_file
        self.query = query
        self.params = params

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

# Usage
query = "SELECT * FROM users WHERE age > ?"
params = (25,)
with ExecuteQuery("users.db", query, params) as users:
    print(users)
