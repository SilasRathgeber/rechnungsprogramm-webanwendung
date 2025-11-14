# database_config.py

import sqlite3
from datetime import datetime
from backend.config import db_path

# ---------- Adapter ----------
# Adapter = wandelt Python-Objekte um, BEVOR sie in die DB geschrieben werden
# Hier: datetime -> String im ISO-Format ("YYYY-MM-DD"), weil SQLite
# kein richtiges DateTime-Feld kennt, sondern nur Text, Zahl oder Real.
def adapt_date(val):
    return val.strftime("%Y-%m-%d")


# ---------- Converter ----------
# Converter = wandelt DB-Werte zurück, NACHDEM sie aus der DB gelesen wurden
# Hier: String "YYYY-MM-DD" -> String im Format "DD.MM.YYYY"
# (Du könntest hier auch ein datetime-Objekt zurückgeben, wenn dir das lieber ist.)
def convert_date(val):
    try:
        # SQLite kann Werte als bytes oder str liefern → normalisieren auf str
        d = val.decode() if isinstance(val, bytes) else val
        # String in datetime-Objekt parsen
        parsed = datetime.strptime(d, "%Y-%m-%d")
        # in dein gewünschtes Anzeigeformat umwandeln
        return parsed.strftime("%d.%m.%Y")
    except Exception:
        # Falls das Feld kein Datum ist (oder NULL), einfach unverändert zurückgeben
        return val


# ---------- Registrierung ----------
# Muss NUR EINMAL am Anfang deines Programms ausgeführt werden (z. B. in main.py)
# Danach kennt sqlite3 diese Regeln global für alle Connections.
sqlite3.register_adapter(datetime, adapt_date)
sqlite3.register_converter("DATE", convert_date)


def get_connection():
    """Erzeugt eine neue DB-Verbindung mit Standard-Settings."""
    conn = sqlite3.connect(
        db_path,
        detect_types=sqlite3.PARSE_DECLTYPES  # <-- wichtig für DATE/TIMESTAMP
    )
    conn.row_factory = sqlite3.Row   # Ergebnisse als dict-artig
    conn.execute("PRAGMA foreign_keys = ON;")  # Fremdschlüssel erzwingen
    return conn