import sqlite3
from faker import Faker
import random
import os

db_path = "univdata.sql"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
"""
)
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT,
        group_id INTEGER,
        FOREIGN KEY (group_id) REFERENCES groups(id)

    )
"""
)


cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS lectors(
        id INTEGER PRIMARY KEY,
        name TEXT
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY,
        name TEXT,
        lector_id INTEGER,
        FOREIGN KEY (lector_id) REFERENCES lectors(id)
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS marks (
        id INTEGER PRIMARY KEY,
        value INTEGER,
        timestamp TEXT,
        subject_id INTEGER,
        student_id INTEGER,
        FOREIGN KEY (subject_id) REFERENCES subjects(id),
        FOREIGN KEY (student_id) REFERENCES students(id)
    )
"""
)

fake = Faker()

for _ in range(50):
    group_id = random.randint(1, 3)  # генеруємо випадкове group_id
    cursor.execute(
        "INSERT INTO students (name, group_id) VALUES (?, ?)", (fake.name(), group_id)
    )


for i in range(1, 4):
    cursor.execute("INSERT INTO groups (name) VALUES (?)", (f"Group {i}",))


for _ in range(5):
    cursor.execute("INSERT INTO lectors (name) VALUES (?)", (fake.name(),))


subject_names = [
    "Mathematics",
    "Physics",
    "Chemistry",
    "Biology",
    "History",
    "Literature",
    "Computer Science",
]

subject_ids = []

for name in subject_names:
    lector_id = random.randint(1, 5)
    cursor.execute(
        "INSERT INTO subjects (name, lector_id) VALUES (?, ?)", (name, lector_id)
    )
    subject_ids.append(cursor.lastrowid)


for student_id in range(1, 51):
    for subject_id in subject_ids:
        value = random.randint(1, 100)
        timestamp = fake.date_time_between(start_date="-1y", end_date="now").strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        cursor.execute(
            "INSERT INTO marks (value, timestamp, subject_id, student_id) VALUES (?, ?, ?, ?)",
            (value, timestamp, subject_id, student_id),
        )

conn.commit()
conn.close()
