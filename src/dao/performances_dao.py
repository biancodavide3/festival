import sqlite3
import logging

def get_db_connection():
    conn = sqlite3.connect("festival.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_numero_performance_pubblicate():
    try:
        sql = "SELECT COUNT(*) FROM performances WHERE pubblicato = 1"
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            n = cursor.fetchone()[0]
            cursor.close()
        return n
    except sqlite3.Error as e:
        logging.error(f"get_numero_performance_pubblicate: {e}")
        return 0

def get_performances_venerdi():
    try:
        sql = """
        SELECT * FROM performances
        WHERE pubblicato = 1 AND giorno = 'Venerdi'
        ORDER BY orario
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            performances = cursor.fetchall()
            cursor.close()
        return performances
    except sqlite3.Error as e:
        logging.error(f"get_performances_venerdi: {e}")
        return []

def get_performances_sabato():
    try:
        sql = """
        SELECT * FROM performances
        WHERE pubblicato = 1 AND giorno = 'Sabato'
        ORDER BY orario
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            performances = cursor.fetchall()
            cursor.close()
        return performances
    except sqlite3.Error as e:
        logging.error(f"get_performances_sabato: {e}")
        return []

def get_performances_domenica():
    try:
        sql = """
        SELECT * FROM performances
        WHERE pubblicato = 1 AND giorno = 'Domenica'
        ORDER BY orario
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            performances = cursor.fetchall()
            cursor.close()
        return performances
    except sqlite3.Error as e:
        logging.error(f"get_performances_domenica: {e}")
        return []

def get_performances_pubblicate_by_organizzatore(id_organizzatore):
    try:
        sql = "SELECT * FROM performances WHERE id_organizzatore = ? AND pubblicato = 1"
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_organizzatore,))
            performances = cursor.fetchall()
            cursor.close()
        return performances
    except sqlite3.Error as e:
        logging.error(f"get_performances_pubblicate_by_organizzatore: {e}")
        return []

def get_bozze_by_organizzatore(id_organizzatore):
    try:
        sql = "SELECT * FROM performances WHERE id_organizzatore = ? AND pubblicato = 0"
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (id_organizzatore,))
            bozze = cursor.fetchall()
            cursor.close()
        return bozze
    except sqlite3.Error as e:
        logging.error(f"get_bozze_by_organizzatore: {e}")
        return []

def add_bozza(nome_artista, giorno, orario, durata, descrizione, palco, genere, id_organizzatore):
    try:
        sql = """
        INSERT INTO performances (
            nome_artista, giorno, orario, durata, descrizione, palco, genere, pubblicato, id_organizzatore
        ) VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?)
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql, (
                nome_artista, giorno, orario, durata, descrizione, palco, genere, id_organizzatore
            ))
            conn.commit()
            cursor.close()
        return True
    except sqlite3.Error as e:
        logging.error(f"add_bozza: {e}")
        return False

def publish_bozza(id_performance, id_organizzatore):
    try:
        sql_check = "SELECT pubblicato FROM performances WHERE id = ? AND id_organizzatore = ?"
        sql_update = "UPDATE performances SET pubblicato = 1 WHERE id = ? AND id_organizzatore = ? AND pubblicato = 0"

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_check, (id_performance, id_organizzatore))
            row = cursor.fetchone()
            if row and row["pubblicato"] == 0:
                cursor.execute(sql_update, (id_performance, id_organizzatore))
                conn.commit()
                published = True
            else:
                published = False
            cursor.close()
        return published
    except sqlite3.Error as e:
        logging.error(f"publish_bozza: {e}")
        return False

def delete_bozza(id_performance, id_organizzatore):
    try:
        sql_check = "SELECT pubblicato FROM performances WHERE id = ? AND id_organizzatore = ?"
        sql_delete = "DELETE FROM performances WHERE id = ? AND id_organizzatore = ? AND pubblicato = 0"

        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_check, (id_performance, id_organizzatore))
            row = cursor.fetchone()
            if row and row["pubblicato"] == 0:
                cursor.execute(sql_delete, (id_performance, id_organizzatore))
                conn.commit()
                deleted = True
            else:
                deleted = False
            cursor.close()
        return deleted
    except sqlite3.Error as e:
        logging.error(f"delete_bozza: {e}")
        return False

def update_performance_if_non_pubblicata(id_performance, id_organizzatore, nome_artista, giorno, orario, durata, descrizione, palco, genere):
    try:
        sql_check = "SELECT pubblicato FROM performances WHERE id = ? AND id_organizzatore = ?"
        sql_update = """
            UPDATE performances
            SET nome_artista = ?, giorno = ?, orario = ?, durata = ?, descrizione = ?, palco = ?, genere = ?
            WHERE id = ? AND id_organizzatore = ? AND pubblicato = 0
        """
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql_check, (id_performance, id_organizzatore))
            row = cursor.fetchone()
            if row and row["pubblicato"] == 0:
                cursor.execute(sql_update, (nome_artista, giorno, orario, durata, descrizione, palco, genere, id_performance, id_organizzatore))
                conn.commit()
                updated = True
            else:
                updated = False
            cursor.close()
        return updated
    except sqlite3.Error as e:
        logging.error(f"update_performance_if_non_pubblicata: {e}")
        return False
