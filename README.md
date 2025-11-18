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

# Python Generators - Task 1

## Objective
Create a Python generator to stream rows from the `user_data` table in the `ALX_prodev` MySQL database.

## Files
- `0-stream_users.py` : Contains the generator function `stream_users()`.
- `1-main.py` : Script to test the generator by printing the first 6 rows.
- `seed.py` : Task 0 database setup (ensure this exists and runs successfully).
- `user_data.csv` : Sample data used to populate the database.

## Usage
1. Ensure Task 0 (seed.py) has been run and database `ALX_prodev` exists.
2. Activate your virtual environment:
```bash
source venv/Scripts/activate  # Windows PowerShell
