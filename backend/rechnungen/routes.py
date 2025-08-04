from flask import Blueprint, request, render_template, redirect, url_for
import sqlite3
import os
from backend.config import db_path
from backend.common import get_all_kunden
from backend.rechnungsprogramm.main import main

rechnungen_bp = Blueprint("rechnungen", __name__)

@rechnungen_bp.route("/rechnungen", methods=["GET", "POST"])
def rechnungen_seite():
    datei_name = None
    
    if request.method == "POST":
        aktion = request.form.get("aktion")
        if aktion == "RechnungErstellen":
            zeiterfassungs_id = request.form.get("id")
            datei_name = main(zeiterfassungs_id)

    


    return render_template(
        "rechnungen.html",
        datei_name=datei_name
    )
