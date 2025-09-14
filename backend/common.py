import sqlite3
from flask import render_template
from backend.config import db_path
from datetime import datetime, date

def get_all_kunden():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, name, strasse, hausnummer, plz, ort, aktueller_stundensatz, email FROM kunden")
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
        print(f"aus load_zeiterfassung_by_id({row_dict['id']}) - > stundensatz {row_dict['stundensatz']}")
        print(f"aus load_zeiterfassung_by_id({row_dict['id']}) - > stunden: {row_dict['stunden']}")
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

def get_kunde(kundennummer):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kunden WHERE id = ?", (kundennummer,))
    result = cursor.fetchone()  # nur einen Datensatz holen
    conn.close()
    
    if result:
        return dict(result)  # z.B. kunde["name"]
    else:
        return None

def getRechnungenWithOrWithout_KundenId(kundennummer=None):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if kundennummer:
       c.execute("""
        SELECT r.id,
            z.id AS zeiterfassung_id,
            z.von AS zeiterfassung_von,
            z.bis AS zeiterfassung_bis,
            r.projekt,
            r.abrechnungsart,
            r.honorar,
            r.erstellt,
            r.re_datum,
            r.verschickt,
            r.ausgangsdatum,
            r.bezahlt,
            IFNULL(ze_sum.gesamt, 0) AS gesamt
        FROM rechnungen r
        LEFT JOIN zeiterfassungen z ON z.rechnung_id = r.id
        LEFT JOIN (
            SELECT z.rechnung_id, SUM(ze.gesamt) AS gesamt
            FROM zeiterfassungen z
            LEFT JOIN zeiteintraege ze ON ze.zeiterfassung_id = z.id
            GROUP BY z.rechnung_id
        ) AS ze_sum ON ze_sum.rechnung_id = r.id
        WHERE r.kunde_id = ?
        ORDER BY r.id DESC;
        """, (kundennummer,))
    else:
        c.execute("""
        SELECT r.kunde_id, 
            r.id,
            z.id AS zeiterfassung_id,
            z.von AS zeiterfassung_von,
            z.bis AS zeiterfassung_bis,
            r.projekt,
            r.abrechnungsart,
            r.honorar,
            r.erstellt,
            r.re_datum,
            r.verschickt,
            r.ausgangsdatum,
            r.bezahlt,
            IFNULL(ze_sum.gesamt, 0) AS gesamt
        FROM rechnungen r
        LEFT JOIN zeiterfassungen z ON z.rechnung_id = r.id
        LEFT JOIN (
            SELECT z.rechnung_id, SUM(ze.gesamt) AS gesamt
            FROM zeiterfassungen z
            LEFT JOIN zeiteintraege ze ON ze.zeiterfassung_id = z.id
            GROUP BY z.rechnung_id
        ) AS ze_sum ON ze_sum.rechnung_id = r.id
        ORDER BY r.id DESC;
        """)
    rows = c.fetchall()
    conn.close()

    columns = rows[0].keys() if rows else []
    data = [dict(row) for row in rows]

    return columns, data

def deleteRechnungen(reNr):
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")  # <-- wichtig!
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    if reNr:
        c.execute("DELETE FROM rechnungen WHERE id = ?", (reNr,))
        conn.commit()
    conn.close()

def get_kundennr_via_reNr(rechnungsnummer):
    conn = sqlite3.connect(db_path)
    # conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT kunde_id FROM rechnungen WHERE id = ?", (rechnungsnummer,))
    result = cursor.fetchone()  # nur einen Datensatz holen
    conn.close()
    
    if result:
        return result[0]
    else:
        return None

def get_rechnung_via_reNr(rechnungsnummer):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            r.*,
            z.id AS zeiterfassung_id,
            z.von,
            z.bis,
            z.stundensatz,
            COUNT(e.id) AS anzahl_zeiteintraege,
            COALESCE(SUM(e.gesamt), 0) AS summe_gesamt
        FROM rechnungen r
        LEFT JOIN zeiterfassungen z 
            ON r.id = z.rechnung_id
        LEFT JOIN zeiteintraege e
            ON z.id = e.zeiterfassung_id
        WHERE r.id = ?
        GROUP BY r.id, z.id;
    """, (rechnungsnummer,))
    result = cursor.fetchone()  # nur einen Datensatz holen
    conn.close()
    
    if result:
        return dict(result)  # z.B. kunde["name"]
    else:
        return None


def set_rechnung_erstellt(rechnungsnummer, name, pfad, rechnungsdatum):
    conn = sqlite3.connect(db_path)
    # conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("UPDATE rechnungen SET erstellt = 1, dateiname = ?, dateipfad = ?, re_datum = ? WHERE id = ?", (name, pfad, rechnungsdatum, rechnungsnummer,))
    conn.commit()
    conn.close()
    

def set_rechnung_versendet(rechnungsnummer):
    heute = date.today()
    conn = sqlite3.connect(db_path)
    # conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("UPDATE rechnungen SET verschickt = 1, ausgangsdatum = ? WHERE id = ?", (heute, rechnungsnummer,))
    conn.commit()
    conn.close()