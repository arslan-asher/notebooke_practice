# test_script.py
import os
import sys

def calculate_average(numbers):
    # Potential ZeroDivisionError if list is empty
    total = sum(numbers)
    return total / len(numbers)

def fetch_user_data(user_id):
    # Intentional unhandled mock error
    query = f"SELECT * FROM users WHERE id = {user_id}" # Direct string formatting vulnerability
    print("Executing query:", query)
    return None