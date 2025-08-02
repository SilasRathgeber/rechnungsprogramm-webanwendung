from flask import Blueprint, request, render_template, redirect, url_for
import sqlite3
import os
from backend.config import db_path
from backend.common import get_all_kunden, get_all_zeiterfassungen, get_zeiterfassungen_fuer_kunden

zeiterfassung_bp = Blueprint("zeiterfassung", __name__)

@zeiterfassung_bp.route("/zeiterfassung", methods=["GET", "POST"])
def zeiterfassung_seite():
    kunden = get_all_kunden()  # Alle Kunden für das Dropdown

    kunde_ausw_id = None
    if request.method == 'POST':
        kunde_ausw_id = request.form.get('kunde_ausw_id')

    if kunde_ausw_id:
        columns, data = get_zeiterfassungen_fuer_kunden(kunde_ausw_id)
    else:
        columns, data = get_all_zeiterfassungen()

    return render_template('zeiterfassung.html', kunden=kunden, columns=columns, data=data)