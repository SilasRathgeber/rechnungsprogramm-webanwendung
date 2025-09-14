import os
import calendar
from datetime import date



ONEDRIVE = "/mnt/onedrive"
GEWERBE = os.path.join(ONEDRIVE, "Eigene Dokumente", "Kleingewerbe - Silas Rathgeber IT-Dienstleistungen")
AUSGANGSRECHNUNGEN = os.path.join(GEWERBE, "Ausgangsrechnungen")

def check_pfad(pfad):
    """
    Prüft, ob der Pfad existiert, und erstellt ihn falls nicht.
    Gibt den Pfad zurück.
    """
    try:
        os.makedirs(pfad, exist_ok=True)
        return pfad
    except Exception as e:
        print(f"Pfad konnte nicht erstellt werden: {e}")
        return None


def find_pfad(rechnungsdatum: date) -> str:
    """
    Erzeugt einen Pfadstring aus einem Datum-Tupel (jahr, monat),
    wobei der Monat als Name ausgegeben wird.
    """
    jahr = rechnungsdatum.year
    monat_name = calendar.month_name[rechnungsdatum.month]  # gibt z.B. "August"

    pfad = os.path.join(AUSGANGSRECHNUNGEN, str(jahr), monat_name)
    check_pfad(pfad)
    return pfad
