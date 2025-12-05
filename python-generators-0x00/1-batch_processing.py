#!/usr/bin/python3
import seed


def stream_users_in_batches(batch_size):
    """Generator that yields users in batches of size batch_size."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)

    # get total number of rows
    cursor.execute("SELECT COUNT(*) FROM user_data")
    total = cursor.fetchone()['COUNT(*)']

    offset = 0
    while offset < total:  # LOOP 1
        cursor.execute(
            f"SELECT * FROM user_data LIMIT {batch_size} OFFSET {offset}"
        )
        rows = cursor.fetchall()
        if not rows:
            break
        yield rows  # yield the batch
        offset += batch_size

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """Process batches and print users with age > 25."""
    for batch in stream_users_in_batches(batch_size):  # LOOP 2
        for user in batch:  # LOOP 3
            if user['age'] > 25:
                print(user)
