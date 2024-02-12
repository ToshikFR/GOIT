try:
    cursor.execute(
        "SELECT s.id AS student_id, s.name AS student_name, m.value AS mark FROM students s JOIN marks m ON s.id = m.student_id JOIN subjects sub ON sub.id = m.subject_id JOIN groups g ON s.group_id = g.id WHERE sub.name = 'Physics' AND g.id = '2'; "
    )
    rows = cursor.fetchall()
    print(rows)
except sqlite3.Error as e:
    print(e)
finally:
    cursor.close()