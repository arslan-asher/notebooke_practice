import os

def process_data(file_path):
    # Bug: Resource leak (opened file without context manager)
    f = open(file_path, 'r')
    data = f.read()

    # Hardcoded sensitive data risk
    api_token = "12345-SECRET-TOKEN"

    return data