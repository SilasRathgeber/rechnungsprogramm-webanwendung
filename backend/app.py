from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import os
from backend.kunden.routes import kunden_bp
from backend.zeiterfassung.routes import zeiterfassung_bp
from backend.rechnungen.routes import rechnungen_bp, pdf_bp
import logging
logging.basicConfig(level=logging.INFO)


app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "dev_secret_key")
app.register_blueprint(kunden_bp)
app.register_blueprint(zeiterfassung_bp)
app.register_blueprint(rechnungen_bp)
app.register_blueprint(pdf_bp)
app.debug = True

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=5002, debug=True, use_reloader=False)

