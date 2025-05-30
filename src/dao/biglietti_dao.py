import sqlite3
import logging

def get_db_connection():
    conn = sqlite3.connect("festival.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_numero_totale_biglietti():
    try:
        sql = "SELECT COUNT(*) FROM biglietti"
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            totale = cursor.fetchone()[0]
            cursor.close()
        return totale
    except sqlite3.Error as e:
        logging.error(f"get_numero_totale_biglietti: {e}")
        return 0

def get_statistiche_biglietti_per_giorno():
    try:
        sql = """
            SELECT giorno, COUNT(*) as totale
            FROM biglietti_giorni
            GROUP BY giorno
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            stats = cursor.fetchall()
            cursor.close()

        risultato = {}
        for row in stats:
            risultato[row['giorno']] = row['totale']
        return risultato
    except sqlite3.Error as e:
        logging.error(f"get_statistiche_biglietti_per_giorno: {e}")
        return {}

def get_biglietto_by_partecipante(id_partecipante):
    try:
        sql = """
        SELECT b.id, b.id_partecipante, b.tipo, b.data_acquisto, bg.giorno
        FROM biglietti b
        LEFT JOIN biglietti_giorni bg ON b.id = bg.id_biglietto
        WHERE b.id_partecipante = ?
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_partecipante,))
            righe = cursor.fetchall()
            cursor.close()

        if not righe:
            return None  

        giorni = [r["giorno"] for r in righe if r["giorno"]]

        biglietto = {
            "id": righe[0].get('id', ''),
            "id_partecipante": righe[0]["id_partecipante"],
            "tipo": righe[0]["tipo"],
            "data_acquisto": righe[0]["data_acquisto"],
            "giorni": giorni
        }
        return biglietto
    except sqlite3.Error as e:
        logging.error(f"get_biglietto_by_partecipante: {e}")
        return None

def add_biglietto(id_partecipante:int, tipo, giorni):
    try:
        sql_biglietto = "INSERT INTO biglietti (id_partecipante, tipo) VALUES (?, ?)"
        sql_giorni = "INSERT INTO biglietti_giorni (id_biglietto, giorno) VALUES (?, ?)"
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_biglietto, (id_partecipante, tipo))
            id_biglietto = cursor.lastrowid
            for giorno in giorni:
                cursor.execute(sql_giorni, (id_biglietto, giorno))
            conn.commit()
            cursor.close()
        return True
    except sqlite3.Error as e:
        logging.error(f"add_biglietto: {e}")
        return False
