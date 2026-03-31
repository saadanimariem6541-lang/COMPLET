import sqlite3
from config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """Initialise la base de données avec la colonne type_vehicule si elle n'existe pas"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Créer la table si elle n'existe pas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS acces (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            matricule TEXT NOT NULL,
            date_heure TEXT NOT NULL,
            statut TEXT NOT NULL,
            type_vehicule TEXT
        )
    """)
    
    # Vérifier si la colonne type_vehicule existe
    cursor.execute("PRAGMA table_info(acces)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'type_vehicule' not in columns:
        cursor.execute("ALTER TABLE acces ADD COLUMN type_vehicule TEXT")
        print("✅ Colonne 'type_vehicule' ajoutée à la base de données")
    
    conn.commit()
    conn.close()

def enregistrer_acces(matricule, date_heure, statut, type_vehicule=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO acces (matricule, date_heure, statut, type_vehicule)
        VALUES (?, ?, ?, ?)
    """, (matricule, date_heure, statut, type_vehicule))

    conn.commit()
    conn.close()

def get_all_acces():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT matricule, date_heure, statut, type_vehicule
        FROM acces
        ORDER BY date_heure DESC
        LIMIT 50
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows