from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, "../rechnungsprogramm_database.db")

def get_all_kunden():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name, strasse, hausnummer, plz, ort, stundensatz FROM kunden")
    kunden = c.fetchall()
    conn.close()
    return kunden

@app.route("/kunden", methods=["GET", "POST"])
def kunden_seite():
    if request.method == "POST":
        data = request.form
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute(
            "INSERT INTO kunden (name, strasse, hausnummer, plz, ort, stundensatz) VALUES (?, ?, ?, ?, ?, ?)",
            (data['name'], data['strasse'], data['hausnummer'], data['plz'], data['ort'], data['stundensatz'])
        )
        conn.commit()
        conn.close()
        # Nach dem Speichern zurück zur Kunden-Seite mit GET (Post/Redirect/Get Pattern)
        return redirect(url_for('kunden_seite'))
    
    # Für GET: Kunden aus DB holen und Formular + Liste rendern
    kunden = get_all_kunden()
    return render_template("kunden.html", kunden=kunden)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="127.0.0.1", port=8000, debug=True)
