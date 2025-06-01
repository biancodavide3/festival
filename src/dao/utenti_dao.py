import sqlite3
import logging

def get_db_connection():
    conn = sqlite3.connect("festival.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_utente_by_id(id):
    try:
        sql = "SELECT * FROM utenti WHERE id = ?"
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id,))
            utente = cursor.fetchone()
            cursor.close()
        return utente
    except sqlite3.Error as e:
        logging.error(f"get_utente_by_id: {e}")
        return None

def get_utente_by_email(email):
    try:
        sql = "SELECT * FROM utenti WHERE email = ?"
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (email,))
            utente = cursor.fetchone()
            cursor.close()
        return utente
    except sqlite3.Error as e:
        logging.error(f"get_utente_by_email: {e}")
        return None

def add_utente(nome, cognome, email, password, ruolo):
    try:
        sql = "INSERT INTO utenti (nome, cognome, email, password, ruolo) VALUES (?, ?, ?, ?, ?)"
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (nome, cognome, email, password, ruolo))
            user_id = cursor.lastrowid
            conn.commit()
            cursor.close()
        if user_id:
            return user_id
        return None
    except sqlite3.Error as e:
        logging.error(f"add_utente: {e}")
        return None

def get_numero_organizzatori():
    try:
        sql = "SELECT COUNT(*) FROM utenti WHERE ruolo = 'organizzatore'"
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            n = cursor.fetchone()[0]
            cursor.close()
        return n
    except sqlite3.Error as e:
        logging.error(f"get_numero_organizzatori: {e}")
        return 0

def get_numero_partecipanti():
    try:
        sql = "SELECT COUNT(*) FROM utenti WHERE ruolo = 'partecipante'"
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            n = cursor.fetchone()[0]
            cursor.close()
        return n
    except sqlite3.Error as e:
        logging.error(f"get_numero_partecipanti: {e}")
        return 0
