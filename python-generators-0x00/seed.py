import mysql.connector
import os
import csv
import uuid


def connect_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "Makanaka@1")
    )


def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    cursor.close()


def connect_to_prodev():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "Makanaka@1"),
        database="ALX_prodev"
    )


def create_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        user_id CHAR(36) PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL,
        age DECIMAL NOT NULL,
        INDEX(user_id)
    );
    """)
    cursor.close()


def insert_data(connection, csv_file):
    cursor = connection.cursor()
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
            INSERT IGNORE INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s);
            """, (str(uuid.uuid4()), row['name'], row['email'], row['age']))
    connection.commit()
    cursor.close()


def stream_users(connection):
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    cursor.close()
