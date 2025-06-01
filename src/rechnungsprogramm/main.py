import sys
from rechnungsprogramm.config import *
from rechnungsprogramm.build_invoice import erstelle_rechnung
from rechnungsprogramm.fonts import registriere_schriftarten
from rechnungsprogramm.generate_rechnungsnummer import generate_rechnungsnummer
from rechnungsprogramm.customer import Customer
from rechnungsprogramm.time_report import TimeReport

def get_excel_file_name():
    if len(sys.argv) != 2:
        print("Bitte eine Excel-Datei als Argument übergeben. (Endung .xlsx)")
        sys.exit()
    # Stecke den String, der als erstes Argument übergeben wurde in eine Variable
    excel_datei = sys.argv[1]
    return excel_datei

def main():
    print(f"\nRechnungsprogramm wird ausgeführt...\n")
    registriere_schriftarten()
    rechnungsnummer = generate_rechnungsnummer()
    zeit_protokoll = TimeReport.from_excel(get_excel_file_name())
    

    kunde = Customer.from_excel(KUNDENLISTE, zeit_protokoll.kundennummer)
    kunde.print_tabulated()
    zeit_protokoll.print_time_report()
    datensatz_aus_zeitdatei = zeit_protokoll.content
    report_head_infos = [zeit_protokoll.kundennummer, zeit_protokoll.start_day, zeit_protokoll.stop_day]
    standard_schriftart = "Carlito"
    font_table_head = "CarlitoB"
    erstelle_rechnung(kunde, datensatz_aus_zeitdatei, report_head_infos, rechnungsnummer, standard_schriftart, font_table_head)


if __name__ == "__main__":
    main()