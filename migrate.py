# ATTENZIONE non fa parte dell'applicazione flask in se 
# effettua la migrazione del database allo stato iniziale richiesto dalla consegna
# annullando ogni azione fatta in fase di testing manuale

import sqlite3
import os

if os.path.exists("festival.db"):
    os.remove("festival.db")

conn = sqlite3.connect("festival.db")
cursor = conn.cursor()
with open("migrate.sql", 'r', encoding='utf-8') as f:
    schema_sql = f.read()
cursor.executescript(schema_sql)
conn.commit()
conn.close()
print("Database del festival riconfigurato correttamente!")
