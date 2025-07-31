from flask import Blueprint, request, render_template, redirect, url_for
import sqlite3
import os
from backend.config import db_path
from backend.common import get_all_kunden, get_all_zeiterfassungen

zeiterfassung_bp = Blueprint("zeiterfassung", __name__)

@zeiterfassung_bp.route("/zeiterfassung", methods=["GET", "POST"])
def zeiterfassung_seite():
    if request.method == "POST":
        print("Hallo aus der Post-Methode")



    kunden = get_all_kunden()
    zeiterfassungen = get_all_zeiterfassungen()
    return render_template("zeiterfassung.html", kunden=kunden, zeiterfassungen=zeiterfassungen)