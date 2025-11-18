import sqlite3

# Connect to users.db (creates the file if it doesn't exist)
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create the users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
''')

# Insert sample data
cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com')")
cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (2, 'Bob', 'bob@example.com')")

conn.commit()
conn.close()

print("Database and 'users' table created with sample data.")
