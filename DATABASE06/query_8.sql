try:
    cursor.execute(
        "SELECT l.name, sub.name, AVG(m.value) as average_mark FROM marks m JOIN subjects sub ON sub.id = m.subject_id JOIN lectors l ON sub.lector_id = l.id  WHERE  l.name = 'Todd Warren' ORDER BY average_mark; "
    )
    rows = cursor.fetchall()
    print(rows)
except sqlite3.Error as e:
    print(e)
finally:
    cursor.close()