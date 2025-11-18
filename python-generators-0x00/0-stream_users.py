#!/usr/bin/python3
"""
Task 1: Generator to stream rows from user_data table
"""

import seed  # import your seed.py to connect to database

def stream_users():
    """Generator function that yields user rows one by one."""
    connection = seed.connect_to_prodev()  # connect to ALX_prodev
    if not connection:
        return

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")  # fetch all rows

    # single loop to yield one row at a time
    for row in cursor:
        yield row

    cursor.close()
    connection.close()
