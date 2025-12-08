import sqlite3
import os

# Attenzione non fa parte dell'applicazione flask in se
# serve solo per resettare il db durante lo sviluppo

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "festival.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "migrate.sql")

# rimuove il db esistente
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# ricrea il db
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    schema_sql = f.read()

cursor.executescript(schema_sql)
conn.commit()
conn.close()

print(f"Database del festival resettato correttamente: {DB_PATH}")
