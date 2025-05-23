#!/usr/bin/env python3
"""
A custom context manager for handling a database connection.
"""

import sqlite3


class DatabaseConnection:
    """
    Context manager for SQLite database connections.
    Automatically opens and closes the connection.
    """

    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """Open the database connection and return the cursor."""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor  # return the cursor to execute queries

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commit changes and close the connection."""
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
            self.connection.close()


# Usage example
if __name__ == "__main__":
    # Assume 'users.db' has a table called 'users'
    with DatabaseConnection("users.db") as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
