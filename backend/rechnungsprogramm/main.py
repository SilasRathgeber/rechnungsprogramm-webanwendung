import sys
from datetime import datetime
from .config import *
from .build_invoice import erstelle_rechnung
from .fonts import registriere_schriftarten
from .generate_rechnungsnummer import generate_rechnungsnummer
from .customer import Customer
from .time_report import TimeReport
from .invoice import Invoice

def get_excel_file_name():
    if len(sys.argv) != 2:
        print("Bitte eine Excel-Datei als Argument übergeben. (Endung .xlsx)")
        sys.exit()
    # Stecke den String, der als erstes Argument übergeben wurde in eine Variable
    excel_datei = sys.argv[1]
    return excel_datei

def main(zeiterfassungs_id, vorschau: int):
    print(f"\nRechnungsprogramm wird ausgeführt...\n")
    registriere_schriftarten()
    rechnungsnummer = generate_rechnungsnummer()
    jetzt = datetime.now()
    rechnungsdatum = jetzt.date()
    zeit_protokoll = TimeReport.from_sql(zeiterfassungs_id)
    

    kunde = Customer.from_sqlite(zeiterfassungs_id)
    kunde.print_tabulated()
    zeit_protokoll.print_time_report()
    report_head_infos = [zeit_protokoll.kundennummer, zeit_protokoll.start_day, zeit_protokoll.stop_day]
    standard_schriftart = "Carlito"
    font_table_head = "CarlitoB"
    rechnung = Invoice(kunde, zeit_protokoll, rechnungsdatum)
    datei_name = erstelle_rechnung(vorschau, kunde, rechnung, report_head_infos, rechnungsnummer, standard_schriftart, font_table_head)

    return datei_name

if __name__ == "__main__":
    main()