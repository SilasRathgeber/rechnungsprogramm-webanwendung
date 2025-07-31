from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import os
from backend.kunden.routes import kunden_bp
from backend.zeiterfassung.routes import zeiterfassung_bp

app = Flask(__name__, template_folder="templates")
app.register_blueprint(kunden_bp)
app.register_blueprint(zeiterfassung_bp)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="127.0.0.1", port=8000, debug=True, use_reloader=False)

