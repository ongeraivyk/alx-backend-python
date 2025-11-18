#!/usr/bin/python3
"""
Task 3: Lazy loading paginated data from user_data table using a generator.
"""

# import the seed module
seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database using LIMIT and OFFSET.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """
    Generator that yields pages of users lazily.
    Only one page is in memory at a time.
    """
    offset = 0
    while True:
        rows = paginate_users(page_size, offset)
        if not rows:
            break
        yield rows
        offset += page_size
