# Python Generators Project

## Overview
This project demonstrates advanced usage of **Python generators** to handle large datasets efficiently.  
It includes tasks for streaming data from a database, batch processing, lazy pagination, and memory-efficient aggregation.

Generators allow iterative access to data, promoting optimal resource utilization and improved performance in data-driven applications.

---

## Table of Contents
- [Tasks](#tasks)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Learning Outcomes](#learning-outcomes)

---

## Tasks

### **Task 0: Setting up the database (`seed.py`)**
- Connects to the MySQL server.
- Creates the database `ALX_prodev` if it doesn’t exist.
- Creates the table `user_data` with fields:
  - `user_id` (UUID, Primary Key, Indexed)
  - `name` (VARCHAR, NOT NULL)
  - `email` (VARCHAR, NOT NULL)
  - `age` (DECIMAL, NOT NULL)
- Populates the table with sample data from `user_data.csv`.
- Verified database and first 5 rows.

**Files:** `seed.py`, `0-main.py`

---

### **Task 1: Generator that streams rows from SQL database**
- Implemented a **generator function** `stream_users()` to fetch rows one by one.
- Uses the `yield` keyword to iterate over the `user_data` table **without loading all rows into memory**.
- Demonstrated with `islice()` to fetch only first 6 rows.

**Files:** `0-stream_users.py`, `1-main.py`

---

### **Task 2: Batch processing large data**
- Created a **generator** `stream_users_in_batches(batch_size)` to fetch rows in batches.
- Implemented `batch_processing(batch_size)` to filter users over the age of 25.
- Memory-efficient: only one batch is loaded at a time.
- No more than 3 loops used.

**Files:** `1-batch_processing.py`, `2-main.py`

---

### **Task 3: Lazy loading paginated data**
- Implemented a **generator** `lazy_pagination(page_size)` to simulate paginated data fetching.
- Uses `paginate_users(page_size, offset)` to fetch the next page **only when needed**.
- Only one loop used for lazy evaluation.

**Files:** `2-lazy_paginate.py`, `3-main.py`

---

### **Task 4: Memory-efficient aggregation**
- Implemented a generator `stream_user_ages()` that yields user ages one by one.
- Used the generator to compute **average age** without loading the entire dataset.
- Only two loops used: one for streaming, one for aggregation.
- SQL `AVERAGE` function was **not used**; computation is in Python.

**Files:** `4-stream_ages.py`

---

## Requirements
- Python 3.x
- MySQL Server
- MySQL Connector (`mysql-connector-python` or `pymysql`)
- CSV file: `user_data.csv`

---

## Setup Instructions
1. Clone this repository:
   ```bash
   git clone <your-repo-url>
