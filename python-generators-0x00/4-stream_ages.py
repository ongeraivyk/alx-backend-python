#!/usr/bin/python3
import seed


def stream_user_ages():
    """Generator that yields user ages one by one."""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()

    cursor.execute("SELECT age FROM user_data")

    for (age,) in cursor:  # LOOP 1
        yield int(age)

    cursor.close()
    connection.close()


def compute_average_age():
    """Compute average age using generator — LOOP 2."""
    total = 0
    count = 0

    for age in stream_user_ages():  # LOOP 2
        total += age
        count += 1

    if count == 0:
        average = 0
    else:
        average = total / count

    print(f"Average age of users: {average}")


if __name__ == "__main__":
    compute_average_age()
