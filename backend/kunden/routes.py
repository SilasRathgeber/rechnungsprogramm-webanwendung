from flask import Blueprint, request, render_template, redirect, url_for
import sqlite3
import os
from backend.config import db_path
from backend.common import get_all_kunden

kunden_bp = Blueprint("kunden", __name__)

@kunden_bp.route("/kunden", methods=["GET", "POST"])
def kunden_seite():
    if request.method == "POST":
        aktion = request.form.get("aktion")
        
        if aktion == "hinzufuegen":
            data = request.form
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute(
                "INSERT INTO kunden (name, strasse, hausnummer, plz, ort, stundensatz) VALUES (?, ?, ?, ?, ?, ?)",
                (data['name'], data['strasse'], data['hausnummer'], data['plz'], data['ort'], data['stundensatz'])
            )
            conn.commit()
            conn.close()

        elif aktion == "loeschen":
            kunde_id = request.form.get("kunde_loeschen_id")
            if kunde_id:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute("DELETE FROM kunden WHERE id = ?", (kunde_id,))
                conn.commit()
                conn.close()

        return redirect(url_for('kunden_seite'))
    


    # Für GET: Kunden aus DB holen und Formular + Liste rendern
    kunden = get_all_kunden()
    return render_template("kunden.html", kunden=kunden)
