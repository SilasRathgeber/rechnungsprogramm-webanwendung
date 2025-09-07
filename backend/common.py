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
            z.bis,
            COALESCE(
                (SELECT COUNT(*) 
                FROM zeiteintraege ze 
                WHERE ze.zeiterfassung_id = z.id), 0
            ) as anzahl_zeiteintraege
        FROM
            zeiterfassungen z
        LEFT JOIN
            rechnungen r ON z.rechnung_id = r.id
        WHERE
            z.kunde_id = ?
        ORDER BY
            z.id IS NOT NULL, z.id DESC
    """, (kunde_id,))
    rows = c.fetchall()
    conn.close()

    columns = rows[0].keys() if rows else []
    data = [dict(row) for row in rows]

    return columns, data

def load_zeiterfassung_by_id(id):
    import sqlite3

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Zeiteinträge abrufen
    cursor.execute("SELECT * FROM zeiteintraege WHERE zeiterfassung_id = ?", (id,))
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    data = []
    for row in rows:
        # in dict umwandeln, damit wir schreiben können
        row_dict = dict(row)

        # gesamt berechnen und auf 2 Nachkommastellen runden
        korrektes_gesamt = round(row_dict["stundensatz"] * row_dict["stunden"], 2)
        print(f"korrektes_gesamt: {korrektes_gesamt}")
        # falls der Wert abweicht, DB aktualisieren
        if round(row_dict["gesamt"], 2) != korrektes_gesamt:
            cursor.execute(
                "UPDATE zeiteintraege SET gesamt = ? WHERE id = ?",
                (korrektes_gesamt, row_dict["id"])
            )

        # Wert in dict setzen (immer korrekt)
        row_dict["gesamt"] = korrektes_gesamt
        data.append(row_dict)

    # Änderungen speichern
    conn.commit()
    conn.close()

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

def getRechnungenWithOrWithout_KundenId(kundennummer=None):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if kundennummer:
        c.execute("""
            SELECT r.*, 
                IFNULL(SUM(ze.gesamt), 0) AS gesamt
            FROM rechnungen r
            LEFT JOIN zeiterfassungen z ON z.rechnung_id = r.id
            LEFT JOIN zeiteintraege ze ON ze.zeiterfassung_id = z.id
            WHERE r.kunde_id = ?
            GROUP BY r.id
            ORDER BY r.id DESC
        """, (kundennummer,))
    else:
        c.execute("""
            SELECT r.*, 
                IFNULL(SUM(ze.gesamt), 0) AS gesamt
            FROM rechnungen r
            LEFT JOIN zeiterfassungen z ON z.rechnung_id = r.id
            LEFT JOIN zeiteintraege ze ON ze.zeiterfassung_id = z.id
            GROUP BY r.id
            ORDER BY r.id DESC
        """)
    rows = c.fetchall()
    conn.close()

    columns = rows[0].keys() if rows else []
    data = [dict(row) for row in rows]

    return columns, data


