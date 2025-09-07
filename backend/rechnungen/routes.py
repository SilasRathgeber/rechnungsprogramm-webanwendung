from flask import Blueprint, request, render_template, redirect, url_for
import sqlite3
import os
from backend.config import db_path
from backend.common import get_kundenname, getRechnungenWithOrWithout_KundenId, get_all_kunden
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
                if kunde_id == "":
                    table_columns, table_data = getRechnungenWithOrWithout_KundenId()

            else:
                table_columns, table_data = getRechnungenWithOrWithout_KundenId()


        if aktion == "RechnungSchreiben":
            kunde_id = request.form.get("kunde")
            erfassungs_id = request.form.get("erfassungsId")
            table_columns, table_data = getRechnungenWithOrWithout_KundenId(kunde_id)
            print("aus /rechnungen")
            # datei_name = main(erfassungs_id, 0) # 0 steht für KEINE Vorschau
 
    

    if request.method == "GET":
        kunde_id = request.args.get("kunde", None)
        table_columns, table_data = getRechnungenWithOrWithout_KundenId(kunde_id)

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
