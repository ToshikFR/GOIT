try:
    cursor.execute(
        "SELECT s.id, s.name, g.id  from students s JOIN groups g ON s.group_id = g.id WHERE g.id = '2'; "
    )
    rows = cursor.fetchall()
    print(rows)
except sqlite3.Error as e:
    print(e)
finally:
    cursor.close()