try:
    cursor.execute(
        "SELECT s.id, s.name, AVG(m.value) AS average_mark FROM students s JOIN marks m ON s.id = m.student_id GROUP BY s.id ORDER BY average_mark DESC LIMIT 5;"
        )
    rows = cursor.fetchall()
    print(rows)
except sqlite3.Error as e:
    print(e)
finally:
    cursor.close()
