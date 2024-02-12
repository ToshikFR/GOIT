try:
    cursor.execute(
        "SELECT AVG(m.value) as average_mark FROM marks m  ORDER BY average_mark;"
    )
    rows = cursor.fetchall()
    print(rows)
except sqlite3.Error as e:
    print(e)
finally:
    cursor.close()