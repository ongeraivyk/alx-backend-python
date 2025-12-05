#!/usr/bin/python3
import seed

def stream_users():
    """Generator that yields rows from user_data table one by one."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")

    # ONE loop only
    for row in cursor:
        yield row

    cursor.close()
    connection.close()
