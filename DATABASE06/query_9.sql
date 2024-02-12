try:
    cursor.execute(
        "SELECT m.subject_id, sub.name, s.name FROM marks m JOIN students s ON s.id = m.student_id JOIN subjects sub ON sub.id = m.subject_id  WHERE  s.name = 'Sandra Aguilar'; "
    )
    rows = cursor.fetchall()
    print(rows)
except sqlite3.Error as e:
    print(e)
finally:
    cursor.close()