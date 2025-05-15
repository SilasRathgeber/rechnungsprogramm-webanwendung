# Aufruf des Programms noch über: PYTHONPATH=src python -m rechnungsprogramm.main data/zeiterfassung_januar.xlsx

from rechnungsprogramm.config import *
from rechnungsprogramm.build_invoice import generate_invoice
from rechnungsprogramm.fonts import registriere_schriftarten

registriere_schriftarten()
generate_invoice()