try:
    cursor.execute(
        "SELECT l.name, s.name, AVG(m.value) as average_mark FROM marks m  JOIN students s ON s.id = m.student_id JOIN subjects sub ON sub.id = m.subject_id JOIN lectors l ON sub.lector_id = l.id  WHERE  l.name = 'Todd Warren' AND s.name = 'Sandra Aguilar' ORDER BY average_mark; "
    )
    rows = cursor.fetchall()
    print(rows)
except sqlite3.Error as e:
    print(e)
finally:
    cursor.close()