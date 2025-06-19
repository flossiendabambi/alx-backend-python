import sqlite3
import functools
from datetime import datetime

# ✅ Decorator to log SQL queries with timestamp
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the SQL query
        query = kwargs.get('query') or (args[0] if args else None)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if query:
            print(f"[{timestamp}] Executing SQL query: {query}")
        else:
            print(f"[{timestamp}] No SQL query found to log.")
        
        return func(*args, **kwargs)
    return wrapper

# ✅ Function to fetch users from the database
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# ✅ Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
