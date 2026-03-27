import sqlite3
from config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS acces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricule TEXT NOT NULL,
            date_heure TEXT NOT NULL,
            statut TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def enregistrer_acces(matricule, date_heure, statut):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO acces (matricule, date_heure, statut)
        VALUES (?, ?, ?)
    """, (matricule, date_heure, statut))
    conn.commit()
    conn.close()

def get_all_acces():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT matricule, date_heure, statut
        FROM acces
        ORDER BY date_heure DESC
        LIMIT 50
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows