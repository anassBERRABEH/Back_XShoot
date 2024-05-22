import sqlite3


def drop_all_tables(db_path):
    # Connect to the database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Get the names of all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Drop each table
    for table_name in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name[0]};")
        print(f"Dropped table {table_name[0]}")

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Replace 'your_database.db' with the path to your SQLite database file
drop_all_tables('mydatabase.db')
