import mysql.connector

def connect_to_prodev():
    """Connect to the ALX_prodev MySQL database."""
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Makanaka@1', 
        database='ALX_prodev'
    )

def stream_user_ages():
    """Generator that yields user ages one by one."""
    connection = connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for (age,) in cursor:  # Loop 1
        yield float(age)
    cursor.close()
    connection.close()

def calculate_average_age():
    """Calculates the average age using a generator."""
    total_age = 0
    count = 0
    for age in stream_user_ages():  # Loop 2
        total_age += age
        count += 1
    if count == 0:
        print("No users found.")
    else:
        average = total_age / count
        print(f"Average age of users: {average:.2f}")

# Run the script
if __name__ == "__main__":
    calculate_average_age()
