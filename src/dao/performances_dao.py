import sqlite3

def get_db_connection():
    conn = sqlite3.connect("festival.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_numero_performance_pubblicate():
    sql = "SELECT COUNT(*) FROM performances WHERE pubblicato = 1"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql)
        n = cursor.fetchone()[0]
        cursor.close()
    return n

def get_performances_venerdi():
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

def get_performances_sabato():
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

def get_performances_domenica():
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

def get_performances_pubblicate_by_organizzatore(id_organizzatore):
    sql = "SELECT * FROM performances WHERE id_organizzatore = ? AND pubblicato = 1"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (id_organizzatore,))
        performances = cursor.fetchall()
        cursor.close()
    return performances

def get_bozze_by_organizzatore(id_organizzatore):
    sql = "SELECT * FROM performances WHERE id_organizzatore = ? AND pubblicato = 0"
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, (id_organizzatore,))
        bozze = cursor.fetchall()
        cursor.close()
    return bozze

# ritorna vero o falso se la modifica ha avuto successo o meno
def update_performance_if_non_pubblicata(id_performance, id_organizzatore, nome_artista, giorno, orario, durata, descrizione, palco, genere):
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
