import time
import sqlite3
import functools

# ✅ Decorator to manage DB connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# ✅ Decorator to retry on failure
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"[WARNING] Attempt {attempts} failed: {e}")
                    if attempts < retries:
                        print(f"Retrying in {delay} second(s)...")
                        time.sleep(delay)
                    else:
                        print("[ERROR] All retry attempts failed.")
                        raise
        return wrapper
    return decorator

# ✅ Function using both decorators
@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")  # You can simulate failure here if testing
    return cursor.fetchall()

# ✅ Attempt to fetch users with retry logic
users = fetch_users_with_retry()
print(users)
