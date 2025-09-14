# from .config import INVOICE_LOG
import sqlite3
from backend.config import db_path


def generate_rechnungsnummer(zeiterfassungs_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT rechnung_id FROM zeiterfassungen WHERE id = ?", (zeiterfassungs_id,))
    result = cursor.fetchone()  # nur einen Datensatz holen
    conn.close()
    rechnungsnummer = f"{result[0]:04}"
    return rechnungsnummer


# def generate_rechnungsnummer():
#     with open(INVOICE_LOG, "r", encoding="utf-8") as f:
#         zeilen = f.readlines()

#     letzte_zeile = zeilen[-1]
#     letzte_nummer = int(letzte_zeile)

#     neue_nummer = letzte_nummer + 1


#     # Formatieren mit führenden Nullen
#     formatiert = f"{neue_nummer:04d}"


#     with open(INVOICE_LOG, "a", encoding="utf-8") as f:
#         f.write(f"{formatiert}\n")

#     return(formatiert)