#!/usr/bin/python3
"""
Task 4: Memory-efficient aggregation using Python generators.
Compute average age of users without loading all data at once.
"""

# import seed module to connect to MySQL
seed = __import__('seed')


def stream_user_ages():
    """
    Generator that yields one user age at a time.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    
    for row in cursor:
        yield row['age']
    
    cursor.close()
    connection.close()


def average_age():
    """
    Calculate average age using the generator stream_user_ages.
    """
    total_age = 0
    count = 0
    
    for age in stream_user_ages():
        total_age += age
        count += 1

    if count == 0:
        return 0

    return total_age / count


if __name__ == "__main__":
    avg = average_age()
    print(f"Average age of users: {avg}")
