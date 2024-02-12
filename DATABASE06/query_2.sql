try:
    cursor.execute(
        "SELECT s.id, s.name, MAX(m.value) as max_average_mark FROM students s JOIN marks m ON s.id = m.student_id WHERE m.subject_id = (SELECT id FROM subjects WHERE name = 'Mathematics') GROUP by s.id, s.name ORDER by max_average_mark DESC LIMIT 1 "
    )
    rows = cursor.fetchall()
    print(rows)
except sqlite3.Error as e:
    print(e)
finally:
    cursor.close()