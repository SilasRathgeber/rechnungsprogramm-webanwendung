from flask import Blueprint, request, render_template, redirect, url_for
import sqlite3
import os
from backend.config import db_path
from backend.common import get_all_kunden, get_kundenname, get_kunde

kunden_bp = Blueprint("kunden", __name__)

@kunden_bp.route("/kunden", methods=["GET", "POST"])
def kunden_seite():
    if request.method == "POST":
        aktion = request.form.get("aktion")
        
        if aktion == "hinzufuegen":
            print("hallo aus 'hinzufügen'")
            data = request.form
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute(
                "INSERT INTO kunden (name, strasse, hausnummer, plz, ort, aktueller_stundensatz, email) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (data['name'], data['strasse'], data['hausnummer'], data['plz'], data['ort'], data['stundensatz'], data['email'])
            )
            conn.commit()
            conn.close()

        elif aktion == "bearbeiten":
            kunde_id = request.form.get("kunde_id")
            if kunde_id:
                return redirect(url_for("kunden.kunde_bearbeiten", kunde_id=kunde_id))
        elif aktion == "loeschen":
            kunde_id = request.form.get("kunde_id")
            if kunde_id:
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                c.execute("DELETE FROM kunden WHERE id = ?", (kunde_id,))
                conn.commit()
                conn.close()

        return redirect(url_for("kunden.kunden_seite"))
    


    # Für GET: Kunden aus DB holen und Formular + Liste rendern
    kunden = get_all_kunden()
    return render_template(
        "kunden.html", 
        kunden=kunden)


@kunden_bp.route("/kunden/<int:kunde_id>/bearbeiten", methods=["GET", "POST"])
def kunde_bearbeiten(kunde_id):
    if request.method == "POST":
        aktion = request.form.get("aktion")
        feld = request.form.get("feld")
        kunden_id = int(request.form.get("kunden_id"))
        neuer_wert = request.form.get("neuer_wert")

        def set_kunde_property(kunden_id, feld, neuer_wert):

            erlaubte_felder = ["name", "strasse", "hausnummer", "plz", "ort", "aktueller_stundensatz", "email", "vorlage"]
            if feld not in erlaubte_felder:
                raise ValueError("Ungültiges Feld!")


            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            sql = f"UPDATE kunden SET {feld} = ? WHERE id = ?"
            cursor.execute(sql, (neuer_wert, kunden_id))
            conn.commit()
            conn.close()

        set_kunde_property(kunden_id, feld, neuer_wert)

    kunden_name = get_kundenname(kunde_id)
    kunde = get_kunde(kunde_id)
    return render_template(
        "kunde_bearbeiten.html", 
        kunde_id=kunde_id,
        kunden_name=kunden_name,
        kunde = kunde)