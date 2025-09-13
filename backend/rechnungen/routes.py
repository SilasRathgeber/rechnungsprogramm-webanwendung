from flask import Blueprint, request, render_template, redirect, url_for
import sqlite3
import os
from backend.config import db_path
from backend.common import get_kundenname, getRechnungenWithOrWithout_KundenId, get_all_kunden, deleteRechnungen, get_kundennr_via_reNr, get_rechnung_via_reNr
from backend.rechnungsprogramm.main import main

rechnungen_bp = Blueprint("rechnungen", __name__)

@rechnungen_bp.route("/rechnungen", methods=["GET", "POST"])
def rechnungen_seite():
    datei_name = None
    kunde_id = None
    table_columns = None
    table_data = None
    
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
    # kunde_id = request.args.get("kunde_id")
    if request.method == "POST":
        aktion = request.form.get("aktion")
    

    rechnung = get_rechnung_via_reNr(rechnungsnummer)
    kunde_id = get_kundennr_via_reNr(rechnungsnummer)
    return render_template(
        "rechnung_bearbeiten.html",
        rechnungsnummer=rechnungsnummer,
        kunde_id=kunde_id,
        rechnung=rechnung,
    )
