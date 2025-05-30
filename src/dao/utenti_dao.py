import sqlite3

def get_db_connection():
    conn = sqlite3.connect("festival.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_utente_by_id(id):
    sql = "SELECT * FROM utenti WHERE id = ?"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        utente = cursor.fetchone()
        cursor.close()
    return utente

def get_utente_by_email(email):
    sql = "SELECT * FROM utenti WHERE email = ?"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (email,))
        utente = cursor.fetchone()
        cursor.close()
    return utente

def add_utente(nome, cognome, email, password, ruolo):
    sql = "INSERT INTO utenti (nome, cognome, email, password, ruolo) VALUES (?, ?, ?, ?, ?)"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (nome, cognome, email, password, ruolo))
        conn.commit()
        cursor.close()

def get_numero_organizzatori():
    sql = "SELECT COUNT(*) FROM utenti WHERE ruolo = 'organizzatore'"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        n = cursor.fetchone()[0]
        cursor.close()
    return n

def get_numero_partecipanti():
    sql = "SELECT COUNT(*) FROM utenti WHERE ruolo = 'partecipante'"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        n = cursor.fetchone()[0]
        cursor.close()
    return n
