from flask import Blueprint, request, render_template, redirect, url_for, flash
import sqlite3
import os
from backend.config import db_path
from backend.common import *
from datetime import datetime
import logging
from backend.rechnungsprogramm.main import main

logger = logging.getLogger(__name__)


zeiterfassung_bp = Blueprint("zeiterfassung", __name__)

@zeiterfassung_bp.route("/", methods=["GET", "POST"])
def zeiterfassung_seite():
    kunden = get_all_kunden()         # Dropdown-Daten
    columns, data = [], []            # Tabellenstruktur
    kunde_ausw_id = None              # Vorauswahl
    kunden_name = ""

    if request.method == "POST":
        aktion = request.form.get("aktion")
        kunde_ausw_id = request.form.get("kunde_ausw_id")  # immer lesen
        kunden_name = get_kundenname(kunde_ausw_id)

        if aktion == "filtern":
            if kunde_ausw_id == "" or kunde_ausw_id is None:
                columns, data = get_zeiterfassungen_fuer_kunden()
            else:
                columns, data = get_zeiterfassungen_fuer_kunden(kunde_ausw_id)

        elif aktion == "neuErfassung":
            start = request.form.get("StartDatum")
            end = request.form.get("EndDatum")

            if kunde_ausw_id and start and end:
                with sqlite3.connect(db_path) as conn:
                    cur = conn.cursor()

                    # 1. Rechnung anlegen
                    cur.execute("""
                        INSERT INTO rechnungen (kunde_id, abrechnungsart, projekt, honorar, rechnungsnummer)
                        VALUES (?, ?, ?, ?, ?)
                    """, (kunde_ausw_id, "zeit", None, None, None))

                    rechnung_id = cur.lastrowid   # hier bekommst du die neue ID

                    # 2. Zeiterfassung einfügen und die rechnung_id verwenden
                    cur.execute("""
                        INSERT INTO zeiterfassungen (kunde_id, rechnung_id, von, bis)
                        VALUES (?, ?, ?, ?)
                    """, (kunde_ausw_id, rechnung_id, start, end))

                    conn.commit()
                columns, data = get_zeiterfassungen_fuer_kunden(kunde_ausw_id)

        elif aktion == "löschErfassung":
            zeiterfassung_id = request.form.get("id")

            if zeiterfassung_id:
                with sqlite3.connect(db_path) as conn:
                    conn.execute(
                        "DELETE FROM zeiterfassungen WHERE id = ?", (zeiterfassung_id,)
                    )
            # Tabelle nach Löschung neu laden
            if kunde_ausw_id:
                columns, data = get_zeiterfassungen_fuer_kunden(kunde_ausw_id)

    if request.method == "GET":
        kunde_ausw_id = request.args.get("kunden_id")
        
        columns, data = get_zeiterfassungen_fuer_kunden()

        if kunde_ausw_id:
            
            kunden_name = get_kundenname(kunde_ausw_id)
            
    return render_template(
        'zeiterfassung.html',
        kunden=kunden,
        columns=columns,
        data=data,
        kunde_ausw_id=kunde_ausw_id,
        kunden_name = kunden_name
    )


@zeiterfassung_bp.route("/zeiterfassung/bearbeiten", methods=["GET", "POST"])
def bearbeiten():
    datei_name = None
    if request.method == "GET":
        zeiterfassungs_id = request.args.get('id')
    else:
        zeiterfassungs_id = request.form.get('id')

    if request.method == "POST":
        aktion = request.form.get("aktion")
        
        zeiteintrag_id = request.form.get("eintrag_id")
        logger.info(f"ID im Flask-Backend angekommen: {zeiteintrag_id}")
        logger.info(f"POST-Daten: {dict(request.form)}")
        if aktion == "neuerEintrag":
            datum = request.form.get("datum")
            start_zeit = request.form.get("start_zeit")
            end_zeit = request.form.get("end_zeit")
            beschreibung = request.form.get("beschreibung")

            fmt = "%H:%M"
            start = datetime.strptime(start_zeit, fmt)
            end = datetime.strptime(end_zeit, fmt)
            dauer = end - start
            stunden = dauer.total_seconds() / 3600
            print(f"stunden: {stunden}")

            # Stundensatz aus zeiterfassungen lesen
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()  # <- MUSS innerhalb des Blocks sein
                cursor.execute("SELECT stundensatz FROM zeiterfassungen WHERE id = ?", (zeiterfassungs_id,))
                result = cursor.fetchone()
                logger.info(f"Ergebnis der Datenabfrage für stundensatz: {result}")
                if result is None:
                    return render_template("fehler.html", msg="Kein Stundensatz gefunden"), 400
                    #return "Fehler: Kein Stundensatz gefunden.", 400
                stundensatz = result[0]

                gesamt = round(stunden * stundensatz, 2)
                stunden_round=round(stunden, 3)
                cursor.execute(
                    "INSERT INTO zeiteintraege (zeiterfassung_id, datum, startzeit, endzeit, beschreibung, stunden, stundensatz, gesamt) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (zeiterfassungs_id, datum, start_zeit, end_zeit, beschreibung, stunden_round, stundensatz, gesamt)
                )

        if aktion == "EintragLöschen":
            with sqlite3.connect(db_path) as conn:
                conn.execute(
                    "DELETE FROM zeiteintraege WHERE id = ?", (zeiteintrag_id,)
                )

        if aktion == "set_satz":
            with sqlite3.connect(db_path) as conn:
                zeiterfassungs_id = request.form.get("id")
                neuer_satz = float(request.form.get("new_satz"))
                cursor = conn.cursor() 
                # cursor.execute("UPDATE kunden SET aktueller_stundensatz = ? WHERE id = ( SELECT kunde_id FROM zeiterfassungen WHERE id = ?)", (neuer_satz, zeiterfassungs_id))
                cursor.execute("UPDATE zeiterfassungen SET stundensatz = ? WHERE id = ?", (neuer_satz, zeiterfassungs_id))
                cursor.execute("""UPDATE zeiteintraege SET stundensatz = ? WHERE zeiterfassung_id = ?""", (neuer_satz, zeiterfassungs_id))
                conn.commit()

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT k.* FROM kunden k JOIN zeiterfassungen z ON z.kunde_id = k.id WHERE z.id = ?", (zeiterfassungs_id,))
        kunde = cursor.fetchone()
        cursor.execute("SELECT von, bis, stundensatz FROM zeiterfassungen WHERE id = ?", (zeiterfassungs_id,))
        result = cursor.fetchone()
        if result:
            von, bis, stundensatz = result
            von=date_from_ISO_to_norml(von)
            bis=date_from_ISO_to_norml(bis)

    # GET: Lade die Daten für das Formular
    # z.B. hole aus DB die Zeiterfassung mit der ID
    logger.info(f"Inhalt zeiterfassung_id: {zeiterfassungs_id}")
    
    columns, data = load_zeiterfassung_by_id(zeiterfassungs_id)
 
    if data == "Fehlermeldung":
        flash("Fehler: Die Summe der Zeiteinträge stimmt nicht!", "danger")
        columns, data = [], []  # leere Tabelle anzeigen

    logger.info(f"Inhalt von data und columns: {columns, data}")



    return render_template(
        "zeiterfassung_bearbeiten.html", 
        columns=columns, 
        data=data, 
        zeiterfassungs_id=zeiterfassungs_id, 
        kunde=kunde,
        datei_name=datei_name,
        # zeiterfassung_von=von,
        # zeiterfassung_bis=bis,
        # stundensatz = stundensatz
        )


from flask import request, jsonify
from datetime import datetime

zeiterfassung_ajax = Blueprint("zeiterfassung_ajax", __name__)

@zeiterfassung_ajax.route("/update_row", methods=["POST"])
def update_row():
    data = request.json["row_data"]

    entry_id       = data[0]
    datum          = data[1]
    start          = data[2]
    end            = data[3]
    beschreibung   = data[4]

    conn = db.get_connection()
    cur = conn.cursor()

    # 1) Zeiterfassung-ID + Stundensatz holen
    cur.execute("""
        SELECT zeiterfassung_id, stundensatz 
        FROM zeiteintraege 
        WHERE id = ?
    """, (entry_id,))
    row = cur.fetchone()

    if not row:
        return jsonify({"status": "error", "msg": "Eintrag nicht gefunden"}), 404

    zeiterfassung_id, stundensatz = row

    # Falls stundensatz noch NULL ist → aus zeiterfassungen holen
    if stundensatz is None:
        cur.execute("""
            SELECT stundensatz 
            FROM zeiterfassungen 
            WHERE id = ?
        """, (zeiterfassung_id,))
        ss_row = cur.fetchone()
        stundensatz = ss_row[0] if ss_row else 0.0

    # 2) Stunden berechnen
    try:
        t_start = datetime.strptime(start, "%H:%M")
        t_end   = datetime.strptime(end, "%H:%M")

        diff = (t_end - t_start).total_seconds() / 3600  # Stunden in Dezimal
        if diff < 0:
            diff = 0  # Fallback falls jemand versehentlich 23:00–01:00 eingibt
    except:
        diff = 0

    # 3) Gesamtpreis berechnen
    gesamt = diff * float(stundensatz)

    # 4) UPDATE durchführen
    cur.execute("""
        UPDATE zeiteintraege
        SET datum = ?, 
            startzeit = ?, 
            endzeit = ?, 
            beschreibung = ?, 
            stunden = ?, 
            stundensatz = ?, 
            gesamt = ?
        WHERE id = ?
    """, (datum, start, end, beschreibung, diff, stundensatz, gesamt, entry_id))

    conn.commit()

    return jsonify({
        "status": "ok",
        "stunden": diff,
        "gesamt": gesamt
    })
