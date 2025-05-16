import mysql.connector

def connect_to_prodev():
    """Connect to the ALX_prodev database (adjust params as needed)."""
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Makanaka@1',
        database='ALX_prodev'
    )

def stream_users():
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)  # returns rows as dicts
    cursor.execute("SELECT * FROM user_data")

    # Yield rows one by one with a single loop
    for row in cursor:
        yield row

    cursor.close()
    connection.close()


# Example usage
if __name__ == "__main__":
    for user in stream_users():
        print(user)
