try:
    cursor.execute(
        "SELECT s.id, s.name, l.name as subject_name from subjects s JOIN lectors l ON s.lector_id = l.id WHERE l.name = 'Todd Warren'; "
    )
    rows = cursor.fetchall()
    print(rows)
except sqlite3.Error as e:
    print(e)
finally:
    cursor.close()