import sqlite3
from backend import database_config as db
from flask import render_template
from backend.config import db_path
from datetime import datetime, date

def get_all_kunden():
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, strasse, hausnummer, plz, ort, aktueller_stundensatz, email FROM kunden")
    kunden = c.fetchall()
    conn.close()
    return kunden

def get_all_zeiterfassungen():
    conn = db.get_connection()
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

def get_zeiterfassungen_fuer_kunden(kunde_id=None):
    conn = db.get_connection()
    c = conn.cursor()
    if kunde_id:
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
    else:
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
                ) AS anzahl_zeiteintraege
            FROM
                zeiterfassungen z
            LEFT JOIN
                rechnungen r ON z.rechnung_id = r.id
            ORDER BY
                z.id IS NOT NULL, z.id DESC;
        """)
    rows = c.fetchall()
    conn.close()

    columns = rows[0].keys() if rows else []
    data = [dict(row) for row in rows]

    return columns, data

def load_zeiterfassung_by_id(id):
    conn = db.get_connection()
    cursor = conn.cursor()

    # Zeiteinträge abrufen
    cursor.execute("SELECT * FROM zeiteintraege WHERE zeiterfassung_id = ? ORDER BY datum ASC", (id,))
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    data = []
    for row in rows:
        # in dict umwandeln, damit wir schreiben können
        row_dict = dict(row)

        # gesamt berechnen und auf 2 Nachkommastellen runden
        # print(f"aus load_zeiterfassung_by_id({row_dict['id']}) - > stundensatz {row_dict['stundensatz']}")
        # print(f"aus load_zeiterfassung_by_id({row_dict['id']}) - > stunden: {row_dict['stunden']}")
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
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM kunden WHERE id = ?", (kundennummer,))
    result = cursor.fetchone()  # nur einen Datensatz holen
    conn.close()
    
    if result:
        return result[0]  # erster Wert aus dem Tupel (Spalte "name")
    else:
        return None

def get_kunde(kundennummer):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kunden WHERE id = ?", (kundennummer,))
    result = cursor.fetchone()  # nur einen Datensatz holen
    conn.close()
    
    if result:
        return dict(result)  # z.B. kunde["name"]
    else:
        return None

def getRechnungenWithOrWithout_KundenId(kundennummer=None):
    conn = db.get_connection()
    c = conn.cursor()
    if kundennummer:
       c.execute("""
        SELECT r.id,
            r.rechnungsnummer,
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
        ORDER BY 
            CASE WHEN r.rechnungsnummer IS NULL THEN 0 ELSE 1 END,
            CAST(r.rechnungsnummer AS INTEGER) DESC;
        """, (kundennummer,))
    else:
        c.execute("""
        SELECT r.id,
            r.kunde_id, 
            r.rechnungsnummer,
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
        ORDER BY 
            CASE WHEN r.rechnungsnummer IS NULL THEN 0 ELSE 1 END,
            CAST(r.rechnungsnummer AS INTEGER) DESC;
        """)
    rows = c.fetchall()
    conn.close()

    columns = rows[0].keys() if rows else []
    data = [dict(row) for row in rows]

    return columns, data

def deleteRechnungen(reNr):
    conn = db.get_connection()  
    c = conn.cursor()
    if reNr:
        c.execute("DELETE FROM rechnungen WHERE id = ?", (reNr,))
        conn.commit()
    conn.close()

def get_kundennr_via_reNr(rechnungsnummer):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT kunde_id FROM rechnungen WHERE id = ?", (rechnungsnummer,))
    result = cursor.fetchone()  # nur einen Datensatz holen
    conn.close()
    
    if result:
        return result[0]
    else:
        return None

def get_rechnung_via_reNr(rechnungsnummer):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            r.*,
            z.id AS zeiterfassung_id,
            z.von,
            z.bis,
            z.stundensatz,
            COUNT(e.id) AS anzahl_zeiteintraege,
            ROUND(COALESCE(SUM(e.gesamt), 0), 2) AS summe_gesamt
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


def set_rechnung_erstellt(id, name, pfad, rechnungsdatum):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE rechnungen SET erstellt = 1, dateiname = ?, dateipfad = ?, re_datum = ? WHERE id = ?", (name, pfad, rechnungsdatum, id,))
    conn.commit()
    conn.close()

def set_rechnungsnummer(id, rechnungsnummer):
    print(f'AUS set_rechnungsnummer: das ist "id": {id} und das ist "rechnungsnummer": {rechnungsnummer}')
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE rechnungen SET rechnungsnummer = ? WHERE id = ?", (rechnungsnummer, id,))
    conn.commit()
    conn.close()

def set_neues_rechnungsdatum(id, neues_datum):
    conn = db.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE rechnungen SET re_datum = ? WHERE id = ?",
            (neues_datum, id)
        )
        if cursor.rowcount == 0:
            print(f"Keine Rechnung mit ID: {id} gefunden.")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Fehler beim Aktualisieren des Rechnungsdatums: {e}")
    finally:
        conn.close()

def set_neues_ausgangsdatum(rechnungs_id, ausgangsdatum):
    conn = db.get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE rechnungen SET ausgangsdatum = ?, verschickt = 1 WHERE id = ?",
            (ausgangsdatum, rechnungs_id)
        )
        if cursor.rowcount == 0:
            print(f"Keine Rechnung mit Nummer {rechnungs_id} gefunden.")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Fehler beim Aktualisieren des Ausgangsdatums: {e}")
    finally:
        conn.close()

def set_zahlungsstatus(id, status):
    """
    Setzt bezahlt auf 1 (bezahlt) oder 0 (nicht bezahlt).
    Gibt True zurück, wenn eine Zeile aktualisiert wurde, sonst False.
    """
    conn = db.get_connection()
    cursor = conn.cursor()
    try:
        ziel = 1 if str(status).lower() == "bezahlt" else 0
        cursor.execute(
            "UPDATE rechnungen SET bezahlt = ? WHERE id = ?",
            (ziel, id)
        )
        # rowcount ist bei sqlite3 nach execute verfügbar
        if cursor.rowcount == 0:
            # Keine betroffene Zeile -> Rückmeldung False
            conn.commit()  # commit ist zwar nicht nötig bei 0 Änderungen, ist aber ok
            return False
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        # besser loggen als print in Produktion
        print(f"Fehler beim Aktualisieren des Zahlungsstatus: {e}")
        return False
    finally:
        conn.close()


def set_rechnungspfad(rechnungs_id, pfad, name):
    """
    Setzt den Dateinamen und Pfad einer Rechnung in der Datenbank.

    Gibt True zurück, wenn eine Zeile aktualisiert wurde,
    False, wenn keine Zeile betroffen war.
    """
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE rechnungen SET dateiname = ?, dateipfad = ?, erstellt = 1 WHERE id = ?",
            (name, pfad, rechnungs_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            # Keine Zeile aktualisiert → ID existiert nicht
            print(f"Warnung: Keine Rechnung mit id={rechnungs_id} gefunden.")
            return False
        else:
            print(f"Erfolgreich Rechnung id={rechnungs_id} aktualisiert.")
            return True
    except Exception as e:
        print(f"Fehler beim Aktualisieren der Rechnung: {e}")
        return False
    finally:
        conn.close()

def set_rechnung_versendet(rechnungsnummer):
    heute = date.today()
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE rechnungen SET verschickt = 1, ausgangsdatum = ? WHERE id = ?", (heute, rechnungsnummer,))
    conn.commit()
    conn.close()

def get_all_rechnung_ids():
    conn = db.get_connection()
    c = conn.cursor()
    c.execute("SELECT rechnungsnummer FROM rechnungen")
    result = [row[0] for row in c.fetchall()]  # extrahiere nur die IDs
    conn.close()
    return result

def check_if_rechnung_id_is_occupied(gewünschte_nummer):
    # gewünschte_nummer = int(gewünschte_nummer)
    alle_rechnungsnummern = get_all_rechnung_ids()

    for re_id in alle_rechnungsnummern:
        if re_id == gewünschte_nummer:
            return True  # die gewünschte ID ist schon belegt

    return False  # keine Übereinstimmung gefunden, ID ist frei

def set_rechnungs_id_if_valid(gewünschte_nummer, id):
    validations_ergebnis = check_if_rechnung_id_is_occupied(gewünschte_nummer)

    if validations_ergebnis == True:
        return "error"
    else:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE rechnungen SET rechnungsnummer = ? WHERE id = ?", (gewünschte_nummer, id,))
        conn.commit()
        conn.close()

def naechste_rechnungsnummer_ermitteln():
    conn = db.get_connection()      # Verbindung holen
    cur = conn.cursor()             # Cursor erstellen
    
    cur.execute("SELECT MAX(CAST(rechnungsnummer AS INTEGER)) FROM rechnungen")
    max_reNr = cur.fetchone()[0]

    # 2. Neue Nummer bestimmen
    neue_reNr = 1 if max_reNr is None else max_reNr + 1
    rechnungsnummer_str = f"{neue_reNr:04d}"  # führende Nullen, 4 Stellen

    conn.close()  # Verbindung wieder schließen
    return rechnungsnummer_str

def set_kommentar(rechnungs_id, kommentar):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE rechnungen SET kommentar = ? WHERE id = ?",
        (kommentar, rechnungs_id)
    )
    conn.commit()
    conn.close()


def set_neuen_abrechnungszeitraum(id, von, bis):
    conn = db.get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE zeiterfassungen SET von = ?, bis = ? WHERE rechnung_id = ?",
        (von, bis, id)
    )
    conn.commit()
    conn.close()