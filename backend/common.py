import sqlite3
from backend.config import db_path

def get_all_kunden():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, name, strasse, hausnummer, plz, ort, stundensatz FROM kunden")
    kunden = c.fetchall()
    conn.close()
    return kunden

def get_all_zeiterfassungen():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, kunde_id, typ FROM zeiterfassungen")
    zeiterfassungen = c.fetchall()
    conn.close()
    return zeiterfassungen