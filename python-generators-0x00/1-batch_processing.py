import mysql.connector

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Makanaka@1',
        database='ALX_prodev'
    )

def stream_users_in_batches(batch_size):
    """Yields batches of rows from the user_data table."""
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:  # 1st loop
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch  # yield remaining rows

    cursor.close()
    connection.close()

def batch_processing(batch_size):
    """Processes each batch and yields users older than 25."""
    for batch in stream_users_in_batches(batch_size):  # 2nd loop
        filtered = [user for user in batch if user['age'] > 25]  # 3rd loop
        yield filtered


# Example usage
if __name__ == "__main__":
    for filtered_batch in batch_processing(batch_size=3):
        for user in filtered_batch:
            print(user)

