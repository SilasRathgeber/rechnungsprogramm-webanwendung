from flask import Blueprint, request, render_template, redirect, url_for, send_file, abort
import sqlite3
import os
from backend.config import db_path
from backend.common import get_kundenname, getRechnungenWithOrWithout_KundenId, get_all_kunden, deleteRechnungen, get_kundennr_via_reNr, get_rechnung_via_reNr, set_rechnung_erstellt, get_kunde, set_rechnung_versendet
from backend.rechnungsprogramm.main import main
from backend.mail_script import send_mail
from datetime import date

rechnungen_bp = Blueprint("rechnungen", __name__)

@rechnungen_bp.route("/rechnungen", methods=["GET", "POST"])
def rechnungen_seite():
    kunde_id = None
    table_columns = None
    table_data = None
    datei_name = None
    
    if request.method == "POST":
        print("POST FORM DATA:", request.form)
        aktion = request.form.get("aktion")
        print("Aktion:", aktion)

        if aktion == "filtern":
            kunde_id = request.form.get("kunde_ausw_id")
            if kunde_id:
                # if not kunde_id:
                #     table_columns, table_data = getRechnungenWithOrWithout_KundenId()
                # else:
                print(f"kunde_id bevor die Rechnunge geholt werden { kunde_id }")
                table_columns, table_data = getRechnungenWithOrWithout_KundenId(kunde_id)
                print(f"Aus POST aus atkion:filtern rechnungen - > {table_columns}")
                if kunde_id == "":
                    table_columns, table_data = getRechnungenWithOrWithout_KundenId()

            else:
                table_columns, table_data = getRechnungenWithOrWithout_KundenId()

        elif aktion == "rechnung_loeschen":
            rechnungsnummer = request.form.get("reNr")
            kunde_id = request.form.get("kundenId")

            print(f"Aus 'rechnung_loeschen' im hidden steht: {kunde_id}")
            print(f"Aus 'rechnung_loeschen' im hidden steht: {rechnungsnummer}")
            
            deleteRechnungen(rechnungsnummer)
            return redirect(url_for("rechnungen.rechnungen_seite", kunde_id=kunde_id))
            # table_columns, table_data = getRechnungenWithOrWithout_KundenId(kunde_id)

        elif aktion == "rechnung_detail":
            rechnungsnummer = request.form.get("reNr")
            kunde_id = request.form.get("kundenId")

            print(f"Aus 'rechnung_detail' im hidden steht: {kunde_id}")
            print(f"Aus 'rechnung_detail' im hidden steht: {rechnungsnummer}")

            if kunde_id and rechnungsnummer:
                return redirect(url_for(
                    "rechnungen.rechnung_bearbeiten",
                    rechnungsnummer=rechnungsnummer, 
                    ))

            # return redirect(url_for("rechnungen.rechnungen_seite", kunde_id=kunde_id))

        elif aktion == "RechnungSchreiben":
            kunde_id = request.form.get("kunde")
            erfassungs_id = request.form.get("erfassungsId")
            table_columns, table_data = getRechnungenWithOrWithout_KundenId(kunde_id)
            
            
 
    

    elif request.method == "GET":
        kunde_id = request.args.get("kunde", None)
        table_columns, table_data = getRechnungenWithOrWithout_KundenId(kunde_id or None)
        print(f"Aus GET aus rechnungen - > {table_columns}")


    if kunde_id:
        knd_name = get_kundenname(kunde_id)
    else:
        knd_name = "Unbekannt"

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


@rechnungen_bp.route("/rechnungen/<int:rechnungsnummer>/bearbeiten", methods=["GET", "POST"])
def rechnung_bearbeiten(rechnungsnummer):
    dateiName = None
    datei_name_vorschau = None
    rel_path = None

    if request.method == "POST":
        aktion = request.form.get("aktion")
        if aktion == "RechnungVorschau":
            zeiterfassungs_id = request.form.get("id")
            datei_name_vorschau, pfad, rechnungsdatum = main(zeiterfassungs_id, 1)
        if aktion == "RechnungErstellen":
            zeiterfassungs_id = request.form.get("id")
            reNr = request.form.get("reId")
            dateiName, pfad, rechnungsdatum = main(zeiterfassungs_id, 2)
            # name = datei_name.rsplit('/', 1)[1]
            set_rechnung_erstellt(reNr, dateiName, pfad, rechnungsdatum)
        if aktion == "sendEmail":
            mailInhalt = request.form.get("mailInhalt")
            message = mailInhalt
            rechnung = get_rechnung_via_reNr(rechnungsnummer)
            dateipfad = rechnung['dateipfad']
            kunde = get_kunde(rechnung['kunde_id'])
            empfänger = kunde['email']
            betreff = f"Rechnung {rechnungsnummer} Zeitraum vom {rechnung['von']} bis {rechnung['bis']}"
            success = send_mail(dateipfad, message, empfänger, betreff)

            if success:
                set_rechnung_versendet(rechnungsnummer)

    

    rechnung = get_rechnung_via_reNr(rechnungsnummer)
    if rechnung['erstellt'] == 1:
        # Prüfe ob unter dem Pfad, der in der Datenbank gespeichert ist, auch eine zugehörige PDF vorhand ist wenn ja setze 
        # datei_name so, dass die Datei sofort angezeigt werden kann
        pfad = rechnung['dateipfad']
        
        if pfad is not None:
            if os.path.isfile(pfad):
                print("Datei existiert ✅")
                PDF_FOLDER = "/mnt/onedrive/Eigene Dokumente/Kleingewerbe - Silas Rathgeber IT-Dienstleistungen/Ausgangsrechnungen"
                rel_path = os.path.relpath(pfad, PDF_FOLDER)
            else:
                print("Datei existiert nicht ❌")
  

            

    kunde_id = get_kundennr_via_reNr(rechnungsnummer)
    kunde = get_kunde(kunde_id)
    return render_template(
        "rechnung_bearbeiten.html",
        rechnungsnummer=rechnungsnummer,
        kunde_id=kunde_id,
        rechnung=rechnung,
        datei_name=dateiName,
        datei_name_vorschau=datei_name_vorschau,
        rel_path=rel_path,
        kunde=kunde
    )


pdf_bp = Blueprint("pdf", __name__)

PDF_FOLDER = "/mnt/onedrive/Eigene Dokumente/Kleingewerbe - Silas Rathgeber IT-Dienstleistungen/Ausgangsrechnungen"
@pdf_bp.route("/pdf/<path:filename>")
def serve_pdf(filename):
    file_path = os.path.join(PDF_FOLDER, filename)

    if not os.path.isfile(file_path):
        abort(404)

    return send_file(file_path, mimetype="application/pdf")