try:
    cursor.execute(
        "SELECT g.name as group_name, AVG(m.value) as average_mark FROM groups g JOIN students s ON g.id = s.group_id JOIN marks m ON s.id = m.student_id WHERE m.subject_id = (SELECT id FROM subjects WHERE name = 'Physics') GROUP by g.id, g.name;"
    )
    rows = cursor.fetchall()
    print(rows)
except sqlite3.Error as e:
    print(e)
finally:
    cursor.close()