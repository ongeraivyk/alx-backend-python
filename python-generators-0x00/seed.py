#!/usr/bin/python3
"""
Seed script to create database, create user_data table,
and insert rows from CSV file into MySQL.
"""

import mysql.connector
from mysql.connector import Error
import csv


# ------------------------------------------------------------
# 1. CONNECT TO MYSQL SERVER (NO DATABASE)
# ------------------------------------------------------------
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="kemunto2525"
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None


# ------------------------------------------------------------
# 2. CREATE DATABASE IF NOT EXISTS
# ------------------------------------------------------------
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    connection.commit()
    cursor.close()


# ------------------------------------------------------------
# 3. CONNECT SPECIFICALLY TO ALX_prodev DATABASE
# ------------------------------------------------------------
def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="kemunto2525",
            database="ALX_prodev"
        )
        return connection

    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


# ------------------------------------------------------------
# 4. CREATE user_data TABLE IF NOT EXISTS
# ------------------------------------------------------------
def create_table(connection):
    query = """
    CREATE TABLE IF NOT EXISTS user_data (
        user_id VARCHAR(64) PRIMARY KEY,
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


# ------------------------------------------------------------
# 5. INSERT DATA FROM CSV FILE
# ------------------------------------------------------------
def insert_data(connection, csv_file):
    cursor = connection.cursor()

    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            sql = """
            INSERT IGNORE INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s);
            """
            values = (
                row["user_id"],
                row["name"],
                row["email"],
                row["age"]
            )

            cursor.execute(sql, values)

    connection.commit()
    cursor.close()
