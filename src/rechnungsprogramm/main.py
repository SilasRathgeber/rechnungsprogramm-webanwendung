# Aufruf des Programms noch über: PYTHONPATH=src python -m rechnungsprogramm.main data/zeiterfassung_januar.xlsx

from rechnungsprogramm.config import *
from rechnungsprogramm.build_canvas import built_page
from rechnungsprogramm.table_machine_customer import generate_letter_head_table

generate_letter_head_table()