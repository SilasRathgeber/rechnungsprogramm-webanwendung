# Aufruf des Programms noch über: PYTHONPATH=src python -m rechnungsprogramm.main data/zeiterfassung_januar.xlsx

from rechnungsprogramm.config import *
from rechnungsprogramm.build_canvas import zeichne_briefpapier
from rechnungsprogramm.table_machine_customer import generate_letter_head_table

#zeichne_briefpapier()
generate_letter_head_table()