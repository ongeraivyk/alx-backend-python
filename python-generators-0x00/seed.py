#!/usr/bin/python3
import mysql.connector
import csv
import os

def connect_db():
    """Connect to MySQL server (no database selected)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    """Create ALX_prodev database if it does not exist."""
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    cursor.close()


def connect_to_prodev():
    """Connect specifically to ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    """Create user_data table with required fields."""
    query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(100) PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        age DECIMAL NOT NULL
    );
    """
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    cursor.close()
    print("Table user_data created successfully")


def insert_data(connection, csv_file):
    """Insert CSV data into user_data table."""
    if not os.path.exists(csv_file):
        print(f"{csv_file} not found")
        return

    cursor = connection.cursor()
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
            """, (row["user_id"], row["name"], row["email"], row["age"]))

    connection.commit()
    cursor.close()
