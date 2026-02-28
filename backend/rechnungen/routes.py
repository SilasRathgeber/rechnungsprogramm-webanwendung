from flask import Blueprint, request, render_template, redirect, url_for, send_file, abort, flash
import sqlite3
import os
from backend.config import db_path
from backend.common import *
from backend.rechnungsprogramm.main import main
from backend.mail_script import send_mail
from datetime import date
from werkzeug.utils import secure_filename
import time

rechnungen_bp = Blueprint("rechnungen", __name__)

@rechnungen_bp.route("/rechnungen", methods=["GET", "POST"])
def rechnungen_seite():
    # kunde_id = None
    table_columns = []
    table_data = []
    knd_name = None
    datei_name = None
    
    if request.method == "POST":
        print("POST FORM DATA:", request.form)
        aktion = request.form.get("aktion")
        print("Aktion:", aktion)

        if aktion == "filtern":
            kunde_id = request.form.get("kunde_ausw_id") or None
            print(f"Aus 'filtern' im hidden steht: {kunde_id}")
            return redirect(url_for("rechnungen.rechnungen_seite", 
                kunde_id=kunde_id,
            ))

        elif aktion == "rechnung_loeschen":
            rechnung_id = request.form.get("reNr")
            kunde_id = request.form.get("kundenId")

            deleteRechnungen(rechnung_id)

            if kunde_id == "None":
                return redirect(url_for("rechnungen.rechnungen_seite"))
            else:
                return redirect(url_for("rechnungen.rechnungen_seite", 
                    kunde_id=kunde_id,
                ))
            
        elif aktion == "rechnung_detail":
            id = request.form.get("reNr")
            remindSelectedkunde = request.form.get("kundenId")

            print(f"Aus 'rechnung_detail' im hidden steht: {remindSelectedkunde}")
            print(f"Aus 'rechnung_detail' im hidden steht: {id}")

            if remindSelectedkunde and id:
                return redirect(url_for(
                    "rechnungen.rechnung_bearbeiten",
                    id=id, 
                    remindSelectedkunde= remindSelectedkunde,
                    ))

    elif request.method == "GET":
        selectedKundeReminder = request.args.get("selectedKundeReminder", None)
        if selectedKundeReminder == "None":
            selectedKundeReminder = None
        kunde_id = request.args.get("kunde_id", None)
        kunden_filter = kunde_id or selectedKundeReminder
        table_columns, table_data = getRechnungenWithOrWithout_KundenId(kunden_filter)
        if kunde_id:
            knd_name = get_kundenname(kunde_id)
        else:
            knd_name = None

        print(f"Aus GET aus kunde_id - > {kunde_id}")

    kunden = get_all_kunden()
    
    
    return render_template(
        "rechnungen.html",
        datei_name=datei_name,
        kunde_id=kunde_id,
        knd_name = knd_name,
        table_columns=table_columns,
        table_data=table_data,
        kunden = kunden
    )


@rechnungen_bp.route("/rechnungen/<id>/bearbeiten", methods=["GET", "POST"])
def rechnung_bearbeiten(id):
    # --- Initialwerte für Template ---
    dateiName = None
    datei_name_vorschau = None
    rel_path = None
    selectedKundeReminder = request.args.get("remindSelectedkunde")
    rechnung = get_rechnung_via_reNr(id)
    if rechnung is None:
        flash(f"Rechnung {id} wurde nicht gefunden.", "error")
        return redirect(url_for("rechnungen.uebersicht"))
    dateiName = rechnung['dateiname']
    PDF_FOLDER = "/mnt/onedrive/Eigene Dokumente/Kleingewerbe - Silas Rathgeber IT-Dienstleistungen/Ausgangsrechnungen"
    rechnungsdatum = rechnung['re_datum']
    rechnungszeitraum_von = rechnung['von']
    datum_obj_re_von = datetime.strptime(rechnungszeitraum_von, "%d.%m.%Y")
    jahr = datum_obj_re_von.year
    pdf_pfad_mit_jahr = os.path.join(PDF_FOLDER, str(jahr))

    # --- POST: Aktionen bearbeiten ---
    if request.method == "POST":
        aktion = request.form.get("aktion")

        if aktion == "rechnungsnummerAendern":
            neue_rechnungsnummer = request.form.get("neue-rechnungsnummer")
            aktuelle_rechnungsnummer = request.form.get("aktuelle-rechnungsnummer")
            ergebnis = set_rechnungs_id_if_valid(neue_rechnungsnummer, id)

            if ergebnis == "error":
                flash("Diese Rechnungsnummer ist bereits vergeben!", "error")
                # Zurück auf dieselbe Seite, alte Rechnungsnummer bleibt sichtbar
                return redirect(url_for(
                    "rechnungen.rechnung_bearbeiten",
                    id=id,
                    remindSelectedkunde=selectedKundeReminder
                ))
            else:
                # Erfolgreich geändert → Redirect auf neue Rechnungsnummer
                flash("Rechnungsnummer erfolgreich geändert", "success")
                return redirect(url_for(
                    "rechnungen.rechnung_bearbeiten",
                    id=id,
                    remindSelectedkunde=selectedKundeReminder
                ))


        # 🔹 Vorschau anzeigen (kein Redirect, weil keine dauerhafte Änderung)
        if aktion == "RechnungVorschau":
            zeiterfassungs_id = request.form.get("id")
            


            datei_name_vorschau, pfad, rechnungsdatum = main(zeiterfassungs_id, 1)

            

            selectedKundeReminder = request.args.get("remindSelectedkunde") or request.form.get("remindSelectedkunde")

            # Sicherer Dateiname (verhindert ../ und Sonderzeichen)
            safe_name = secure_filename(datei_name_vorschau)
            # Danach direkt Template rendern (also GET-Teil hier inline ausführen)
            rechnung = get_rechnung_via_reNr(id)
            kunde_id = get_kundennr_via_reNr(id)
            kunde = get_kunde(kunde_id)

            return redirect(url_for(
                "rechnungen.rechnung_bearbeiten",
                id=id,
                remindSelectedkunde=selectedKundeReminder,
                vorschau="1",
                # datei_name_vorschau=safe_name,
                datei_name_vorschau=datei_name_vorschau
            ))


        # 🔹 Rechnung endgültig erstellen (mit Redirect)
        elif aktion == "RechnungErstellen":
            print("Aus ROUTE RechnungErstellen (anfang)")
            rechnungs_id = request.form.get("reId")
            zeiterfassungs_id = request.form.get("id")
            # reNr = request.form.get("reId")
            die_rechnungsnummer = naechste_rechnungsnummer_ermitteln()
            set_rechnungsnummer(rechnungs_id, die_rechnungsnummer)
            dateiName, pfad, rechnungsdatum = main(zeiterfassungs_id, 2)
            set_rechnung_erstellt(id, dateiName, pfad, rechnungsdatum)

            # Nach dem POST → Redirect auf dieselbe Seite (GET)
            return redirect(url_for(
                "rechnungen.rechnung_bearbeiten",
                id=id,
                remindSelectedkunde=selectedKundeReminder
            ))

        elif aktion == "RechnungUeberschreiben":
            zeiterfassungs_id = request.form.get("id")
            rechnungs_id = request.form.get("reId")
            dateiName, pfad, rechnungsdatum = main(zeiterfassungs_id, 2)
            set_rechnung_erstellt(id, dateiName, pfad, rechnungsdatum)
            return redirect(url_for(
                "rechnungen.rechnung_bearbeiten",
                id=id,
                remindSelectedkunde=selectedKundeReminder
            ))

        # 🔹 E-Mail versenden (mit Redirect)
        elif aktion == "sendEmail":
            mailInhalt = request.form.get("mailInhalt")
            rechnung = get_rechnung_via_reNr(id)
            dateipfad = rechnung['dateipfad']
            kunde = get_kunde(rechnung['kunde_id'])
            empfänger = kunde['email']
            betreff = f"Rechnung {rechnung['rechnungsnummer']}, {rechnung['von']} - {rechnung['bis']}"
            success = send_mail(dateipfad, mailInhalt, empfänger, betreff)

            if success:
                set_rechnung_versendet(id)

            return redirect(url_for(
                "rechnungen.rechnung_bearbeiten",
                id=id,
                remindSelectedkunde=selectedKundeReminder
            ))

        elif aktion == "zurueck":
            if selectedKundeReminder == "None":
                return redirect(url_for("rechnungen.rechnungen_seite"))
            else:
                return redirect(url_for("rechnungen.rechnungen_seite", 
                    kunde_id=selectedKundeReminder,
                ))

        elif aktion == "dateipfad_setzen":
            dateiName = request.form.get("dateiname")
            
            # Sicherheitscheck: Nur Dateiname, keine Pfad-Komponenten
            dateiname = os.path.basename(dateiName)
            
            datei_pfad_plus_name = os.path.join(pdf_pfad_mit_jahr, dateiName)
            
            # Prüfen ob Datei wirklich im erlaubten Ordner liegt
            if not datei_pfad_plus_name.startswith(os.path.abspath(pdf_pfad_mit_jahr)):
                return "Ungültiger Dateipfad", 400
            
            # Optional: Prüfen ob Datei existiert
            if not os.path.exists(datei_pfad_plus_name):
                return "Datei nicht gefunden", 404
            
            set_rechnungspfad(rechnung['id'], datei_pfad_plus_name, dateiName)
            
            return redirect(url_for(
                "rechnungen.rechnung_bearbeiten",
                id=id,
                datei_name=dateiName,
                remindSelectedkunde=selectedKundeReminder
            ))
        
        elif aktion == "re_datum_aendern":
            neues_rechnungsdatum = request.form.get("re_datum_neu")
            set_neues_rechnungsdatum(id, neues_rechnungsdatum)
            return redirect(url_for(
                "rechnungen.rechnung_bearbeiten",
                id=id,
                remindSelectedkunde=selectedKundeReminder
            ))
        elif aktion == "ausgangsdatum-setzen":
            ausgangsdatum = request.form.get("ausgangsdatum")
            set_neues_ausgangsdatum(id, ausgangsdatum)
            return redirect(url_for(
                "rechnungen.rechnung_bearbeiten",
                id=id,
                remindSelectedkunde=selectedKundeReminder
            ))
        elif aktion== "zahlung":
            zahlungsstatus = request.form.get("zahlung")
            set_zahlungsstatus(id, zahlungsstatus)
            return redirect(url_for(
                "rechnungen.rechnung_bearbeiten",
                id=id,
                remindSelectedkunde=selectedKundeReminder
            ))
        elif aktion== "kommentar":
            kommentar = request.form.get("kommentar-text")
            set_kommentar(id, kommentar)
            return redirect(url_for(
                "rechnungen.rechnung_bearbeiten",
                id=id,
                remindSelectedkunde=selectedKundeReminder
            ))
        elif aktion== "neuen-abrechnungszeitraum":
            von = request.form.get("von")
            bis = request.form.get("bis")
            set_neuen_abrechnungszeitraum(id, von, bis)
            return redirect(url_for(
                "rechnungen.rechnung_bearbeiten",
                id=id,
                remindSelectedkunde=selectedKundeReminder
            ))


    # --- GET: Seite laden und anzeigen ---
    preview_flag = request.args.get("vorschau")
    datei_name_vorschau = request.args.get("datei_name_vorschau")
    selectedKundeReminder = selectedKundeReminder or request.args.get("remindSelectedkunde")

    # Wenn PDF vorhanden, relativen Pfad bestimmen
    if rechnung and rechnung['erstellt'] == 1:
        pfad = rechnung['dateipfad']
        if pfad and os.path.isfile(pfad):
            print("Datei existiert ✅")
            rel_path = os.path.relpath(pfad, PDF_FOLDER)
        else:
            print("Datei existiert nicht ❌")

    # Ordner anlegen, falls er nicht existiert
    if not os.path.isdir(pdf_pfad_mit_jahr):
        os.makedirs(pdf_pfad_mit_jahr)

    pdfs = [f for f in os.listdir(pdf_pfad_mit_jahr) 
        if f.endswith('.pdf')]

    kunde_id = get_kundennr_via_reNr(id)
    kunde = get_kunde(kunde_id)

    # --- Template rendern ---
    return render_template(
        "rechnung_bearbeiten.html",
        id=id,
        kunde_id=kunde_id,
        rechnung=rechnung,
        datei_name=dateiName,
        datei_name_vorschau=datei_name_vorschau,
        rel_path=rel_path,
        kunde=kunde,
        selectedKundeReminder=selectedKundeReminder,
        ordner=pdfs
    )



pdf_bp = Blueprint("pdf", __name__)

PDF_FOLDER = "/mnt/onedrive/Eigene Dokumente/Kleingewerbe - Silas Rathgeber IT-Dienstleistungen/Ausgangsrechnungen"
@pdf_bp.route("/pdf/<path:filename>")
def serve_pdf(filename):
    file_path = os.path.join(PDF_FOLDER, filename)

    if not os.path.isfile(file_path):
        abort(404)

    return send_file(file_path, mimetype="application/pdf")