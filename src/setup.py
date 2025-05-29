import sqlite3

conn = sqlite3.connect("festival.db")
cursor = conn.cursor()
with open("setup.sql", 'r', encoding='utf-8') as f:
    schema_sql = f.read()
cursor.executescript(schema_sql)
conn.commit()
conn.close()
print("Database del festival configurato correttamente!")
