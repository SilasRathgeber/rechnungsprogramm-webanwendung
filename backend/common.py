import sqlite3
from flask import render_template
from backend.config import db_path
from datetime import datetime

def get_all_kunden():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, name, strasse, hausnummer, plz, ort, aktueller_stundensatz FROM kunden")
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
            r.projekt,
            r.kunde_id AS rechnung_kunde_id,
            r.abrechnungsart,
            r.honorar,
            r.re_datum AS rechnungsdatum
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
            z.id,
            z.kunde_id,
            z.von,
            z.bis
        FROM
            zeiterfassungen z
        LEFT JOIN
            rechnungen r ON z.rechnung_id = r.id
        WHERE
            z.kunde_id = ?
        ORDER BY
            r.re_datum IS NOT NULL, r.re_datum DESC
    """, (kunde_id,))
    rows = c.fetchall()
    conn.close()

    columns = rows[0].keys() if rows else []
    data = [dict(row) for row in rows]

    return columns, data

def load_zeiterfassung_by_id(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM zeiteintraege WHERE zeiterfassung_id = ?", (id,))
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    conn.close()

    data = []
    for row in rows:
        data.append(dict(zip(columns, row)))
    return columns, data

def date_from_ISO_to_norml(date):
    datum_obj = datetime.strptime(date, "%Y-%m-%d")
    datum_lesbar = datum_obj.strftime("%d.%m.%Y")
    return datum_lesbar

def get_kundenname(kundennummer):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM kunden WHERE id = ?", (kundennummer,))
    result = cursor.fetchone()  # nur einen Datensatz holen
    conn.close()
    
    if result:
        return result[0]  # erster Wert aus dem Tupel (Spalte "name")
    else:
        return None

# def select_date_convert(sql_dumb):
