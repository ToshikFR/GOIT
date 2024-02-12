import sqlite3
import logging
import random

db_path = "univdata.sql"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

rows = None

try:
    timestamp = "2024-02-12 12:05:11"
    cursor.execute()
    rows = cursor.fetchall()
    print(rows)
except sqlite3.Error as e:
    print(e)
finally:
    cursor.close()
