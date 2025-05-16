import seed

conn = seed.connect_db()
if conn:
    seed.create_database(conn)
    conn.close()

conn = seed.connect_to_prodev()
if conn:
    seed.create_table(conn)
    seed.insert_data(conn, 'user_data.csv')

    print("Streaming user rows:")
    for user in seed.stream_users(conn):
        print(user)

    conn.close()