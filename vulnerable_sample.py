# Hardcoded secret
AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE_SECRET_KEY"

def query_db(user_input):
    # SQL Injection flaw
    return f"SELECT * FROM users WHERE username = '{user_input}'"
