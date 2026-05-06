import sqlite3
import json

DB_NAME = "crm.db"


# Create table automatically
def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
        )
    """)

    conn.commit()
    conn.close()


# Save latest interaction
def save(data):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO interactions (data) VALUES (?)",
        (json.dumps(data),)
    )

    conn.commit()
    conn.close()

    return data


# Get latest interaction
def get():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT data FROM interactions ORDER BY id DESC LIMIT 1"
    )

    row = cursor.fetchone()

    conn.close()

    if row:

        return json.loads(row[0])

    return {}


# Clear interactions
def clear():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM interactions")

    conn.commit()
    conn.close()

    return {}