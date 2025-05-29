import sqlite3

def get_db_connection():
    conn = sqlite3.connect("festival.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_utente_by_id(id):
    sql = "SELECT * FROM utenti WHERE id = ?"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (id,))
    utente = cursor.fetchone()
    cursor.close()
    conn.close()
    return utente

def get_utente_by_email(email):
    sql = "SELECT * FROM utenti WHERE email = ?"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (email,))
    utente = cursor.fetchone()
    cursor.close()
    conn.close()
    return utente

def add_utente(nome, cognome, email, password, ruolo):
    sql = "INSERT INTO utenti (nome, cognome, email, password, ruolo) VALUES (?, ?, ?, ?, ?)"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(sql, (nome, cognome, email, password, ruolo))
    conn.commit()
    cursor.close()
    conn.close()
