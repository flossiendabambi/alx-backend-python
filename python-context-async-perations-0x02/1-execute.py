#!/usr/bin/env python3
"""
Custom context manager to execute a SQL query
"""

import sqlite3


class ExecuteQuery:
    def __init__(self, query, params=()):
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None

    def __enter__(self):
        # Establish the connection and cursor
        self.conn = sqlite3.connect("my_database.db")
        self.cursor = self.conn.cursor()

        # Execute the query
        self.cursor.execute(self.query, self.params)

        # Fetch results
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the cursor and connection
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)

    with ExecuteQuery(query, param) as result:
        print(result)
