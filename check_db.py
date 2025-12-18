import sqlite3

conn = sqlite3.connect('data/books.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in cursor.fetchall()]
print(f"Tables in database: {tables}")

if 'books' in tables:
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    print(f"\nBooks table has {len(rows)} row(s):")
    for row in rows:
        print(row)

conn.close()
