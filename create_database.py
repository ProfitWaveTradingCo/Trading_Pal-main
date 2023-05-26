import sqlite3
# Establish a connection to the SQLite database
conn = sqlite3.connect('streaming_data.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table to store the streaming data if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS ticks (
        time TEXT,
        volume INTEGER,
        open_price REAL,
        high_price REAL,
        low_price REAL,
        close_price REAL
    )
''')

# Commit the changes to the database
conn.commit()
