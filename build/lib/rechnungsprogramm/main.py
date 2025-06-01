from rechnungsprogramm.config import *
from rechnungsprogramm.build_invoice import erstelle_rechnung
from rechnungsprogramm.get_data import get_kunden_daten, get_time_data_out_of_excel, get_kundennummer_und_zeitraum
from rechnungsprogramm.fonts import registriere_schriftarten
from rechnungsprogramm.generate_rechnungsnummer import generate_rechnungsnummer

def main():
    print("Rechnungsprogramm wird ausgeführt...")
    registriere_schriftarten()
    rechnungsnummer = generate_rechnungsnummer()
    datensatz_aus_kundenliste = get_kunden_daten()
    datensatz_aus_zeitdatei = get_time_data_out_of_excel()
    datensatz_mit_kdr_daten = get_kundennummer_und_zeitraum()
    standard_schriftart = "Carlito"
    font_table_head = "CarlitoB"
    erstelle_rechnung(datensatz_aus_kundenliste, datensatz_aus_zeitdatei, datensatz_mit_kdr_daten, rechnungsnummer, standard_schriftart, font_table_head)
    

if __name__ == "__main__":
    main()