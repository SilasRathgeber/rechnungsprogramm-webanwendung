from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import os

app = Flask(__name__, template_folder="templates")
print("Lade Templates aus:", os.path.abspath(app.template_folder))

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

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    print("Templates werden gesucht in:", os.path.abspath(app.template_folder))
    app.run(host="127.0.0.1", port=8000, debug=True, use_reloader=False)

