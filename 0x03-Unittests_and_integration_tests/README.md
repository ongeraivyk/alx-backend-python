0x03. Unittests and Integration Tests
Project Overview

This project teaches unit and integration testing in Python. You’ll learn how to test functions, classes, and API calls using:

unittest – Python’s built-in testing framework

parameterized – Run tests with multiple inputs

unittest.mock – Mock external dependencies like HTTP requests

Unit tests check individual components, while integration tests verify end-to-end behavior.

Project Structure
0x03-Unittests_and_integration_tests/
├── utils.py          # Helper functions
├── client.py         # GithubOrgClient class
├── fixtures/
│   └── fixtures.py   # Fixture data for integration tests
├── test_utils.py     # Unit tests for utils.py
├── test_client.py    # Unit & integration tests for client.py
└── README.md         # Project documentation

Key Concepts

Unit testing

Integration testing

Parameterized tests

Mocking external calls

Memoization and testing cached properties

Using fixtures for integration tests

Installation

Clone the repository:

git clone https://github.com/<username>/alx-backend-python.git
cd 0x03-Unittests_and_integration_tests


Install dependencies:

pip install parameterized

Running Tests

Run all tests:

python -m unittest discover


Run a specific file:

python -m unittest test_utils.py
python -m unittest test_client.py
