import mysql.connector

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Makanaka@1',
        database='ALX_prodev'
    )

def paginate_users(page_size, offset):
    """Fetch a single page of users from the given offset."""
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
    cursor.execute(query, (page_size, offset))
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    return results

def lazy_paginate(page_size):
    """Generator that lazily paginates through the user_data table."""
    offset = 0
    while True:  # Only one loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


# Example usage
if __name__ == "__main__":
    for page in lazy_paginate(3):
        for user in page:
            print(user)
