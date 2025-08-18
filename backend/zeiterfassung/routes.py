from flask import Blueprint, request, render_template, redirect, url_for
import sqlite3
import os
from backend.config import db_path
from backend.common import get_all_kunden, get_all_zeiterfassungen, get_zeiterfassungen_fuer_kunden, load_zeiterfassung_by_id, date_from_ISO_to_norml
from datetime import datetime
import logging
from backend.rechnungsprogramm.main import main

logger = logging.getLogger(__name__)


zeiterfassung_bp = Blueprint("zeiterfassung", __name__)

@zeiterfassung_bp.route("/zeiterfassung", methods=["GET", "POST"])
def zeiterfassung_seite():
    kunden = get_all_kunden()         # Dropdown-Daten
    columns, data = [], []            # Tabellenstruktur
    kunde_ausw_id = None              # Vorauswahl

    if request.method == "POST":
        aktion = request.form.get("aktion")
        kunde_ausw_id = request.form.get("kunde_ausw_id")  # immer lesen

        if aktion == "filtern":
            if kunde_ausw_id:
                columns, data = get_zeiterfassungen_fuer_kunden(kunde_ausw_id)
            else:
                columns, data = get_all_zeiterfassungen()

        elif aktion == "neuErfassung":
            start = request.form.get("StartDatum")
            end = request.form.get("EndDatum")

            if kunde_ausw_id and start and end:
                with sqlite3.connect(db_path) as conn:
                    conn.execute(
                        "INSERT INTO zeiterfassungen (kunde_id, von, bis) VALUES (?, ?, ?)",
                        (kunde_ausw_id, start, end)
                    )
                columns, data = get_zeiterfassungen_fuer_kunden(kunde_ausw_id)

        elif aktion == "löschErfassung":
            zeiterfassung_id = request.form.get("id")

            if zeiterfassung_id:
                with sqlite3.connect(db_path) as conn:
                    conn.execute(
                        "DELETE FROM zeiteintraege WHERE zeiterfassung_id = ?", (zeiterfassung_id,)
                    )
                    conn.execute(
                        "DELETE FROM zeiterfassungen WHERE id = ?", (zeiterfassung_id,)
                    )
            # Tabelle nach Löschung neu laden
            if kunde_ausw_id:
                columns, data = get_zeiterfassungen_fuer_kunden(kunde_ausw_id)

    if request.method == "GET":
        kunde_ausw_id = request.args.get("kunden_id")

        if kunde_ausw_id:
            columns, data = get_zeiterfassungen_fuer_kunden(kunde_ausw_id)
            
    return render_template(
        'zeiterfassung.html',
        kunden=kunden,
        columns=columns,
        data=data,
        kunde_ausw_id=kunde_ausw_id
    )


@zeiterfassung_bp.route("/zeiterfassung/bearbeiten", methods=["GET", "POST"])
def bearbeiten():
    datei_name = None
    if request.method == "GET":
        zeiterfassungs_id = request.args.get('id')
        zeiterfassung_von = request.args.get('von')
        zeiterfassung_bis = request.args.get('bis')
        zeiterfassung_von_lesbar = date_from_ISO_to_norml(zeiterfassung_von)
        zeiterfassung_bis_lesbar = date_from_ISO_to_norml(zeiterfassung_bis)
        logger.info(f"zeiterfassung_von aus args: {zeiterfassung_von}")
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

            # Stundensatz aus zeiterfassungen lesen
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()  # <- MUSS innerhalb des Blocks sein
                cursor.execute("SELECT k.stundensatz FROM kunden k JOIN zeiterfassungen z ON z.kunde_id = k.id WHERE z.id = ?", (zeiterfassungs_id,))
                result = cursor.fetchone()
                logger.info(f"Ergebnis der Datenabfrage für stundensatz: {result}")
                if result is None:
                    return render_template("fehler.html", msg="Kein Stundensatz gefunden"), 400
                    #return "Fehler: Kein Stundensatz gefunden.", 400
                stundensatz = result[0]

                gesamt = round(stunden * stundensatz, 2)
                stunden_round=round(stunden, 1)
                cursor.execute(
                    "INSERT INTO zeiteintraege (zeiterfassung_id, datum, startzeit, endzeit, beschreibung, stunden, gesamt) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (zeiterfassungs_id, datum, start_zeit, end_zeit, beschreibung, stunden_round, gesamt)
                )

        if aktion == "EintragLöschen":
            with sqlite3.connect(db_path) as conn:
                conn.execute(
                    "DELETE FROM zeiteintraege WHERE id = ?", (zeiteintrag_id,)
                )
        
        if aktion == "RechnungVorschau":
            zeiterfassungs_id = request.form.get("id")
            datei_name = main(zeiterfassungs_id)



    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT k.* FROM kunden k JOIN zeiterfassungen z ON z.kunde_id = k.id WHERE z.id = ?", (zeiterfassungs_id,))
        kunde = cursor.fetchone()
    # GET: Lade die Daten für das Formular
    # z.B. hole aus DB die Zeiterfassung mit der ID
    logger.info(f"Inhalt zeiterfassung_id: {zeiterfassungs_id}")
    columns, data = load_zeiterfassung_by_id(zeiterfassungs_id)
    logger.info(f"Inhalt von data und columns: {columns, data}")



    return render_template(
        "zeiterfassung_bearbeiten.html", 
        columns=columns, 
        data=data, 
        zeiterfassungs_id=zeiterfassungs_id, 
        zeiterfassung_von=zeiterfassung_von_lesbar,
        zeiterfassung_bis=zeiterfassung_bis_lesbar,
        kunde=kunde,
        datei_name=datei_name
        )