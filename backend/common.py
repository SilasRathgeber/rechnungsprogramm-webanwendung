import sqlite3
from flask import render_template
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
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT
            z.*,
            r.zeitraum,
            r.projekt,
            r.kunde_id AS rechnung_kunde_id
        FROM
            zeiterfassungen z
        LEFT JOIN
            rechnungen r ON z.rechnung_id = r.id
    """)
    rows = c.fetchall()
    conn.close()

    columns = rows[0].keys() if rows else [] 
    data = [dict(row) for row in rows]

    return columns, data

def get_zeiterfassungen_fuer_kunden(kunde_id):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("""
        SELECT
            z.*,
            r.zeitraum,
            r.projekt,
            r.kunde_id AS rechnung_kunde_id
        FROM
            zeiterfassungen z
        LEFT JOIN
            rechnungen r ON z.rechnung_id = r.id
        WHERE
            z.kunde_id = ?
    """, (kunde_id,))
    rows = c.fetchall()
    conn.close()

    columns = rows[0].keys() if rows else []
    data = [dict(row) for row in rows]

    return columns, data