# Python Generators – Task 0: Getting Started

## Objective
Create a seeding script that:
- Connects to MySQL
- Creates the database `ALX_prodev`
- Creates the table `user_data`
- Inserts rows from `user_data.csv`

## Files
- `seed.py`
- `user_data.csv`
- `0-main.py`

## Required Functions
1. `connect_db()` – Connects to MySQL server
2. `create_database(connection)` – Creates database if not exists
3. `connect_to_prodev()` – Connects to ALX_prodev
4. `create_table(connection)` – Creates user_data table
5. `insert_data(connection, data)` – Inserts CSV rows

## Running the test
```bash
./0-main.py
