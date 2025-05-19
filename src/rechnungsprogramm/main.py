
from tabulate import tabulate
from rechnungsprogramm.config import *
from rechnungsprogramm.build_invoice import erstelle_rechnung
from rechnungsprogramm.get_data import get_kunden_daten
from rechnungsprogramm.fonts import registriere_schriftarten

registriere_schriftarten()
print(tabulate(get_kunden_daten()))
erstelle_rechnung(get_kunden_daten())
