import pandas as pd
import sys
from rechnungsprogramm.config import DATA_DIR, KUNDENLISTE
from tabulate import tabulate



def get_excel_file_name():
    if len(sys.argv) != 2:
        print("Bitte eine Excel-Datei als Argument übergeben. (Endung .xlsx)")
        sys.exit()
    # Stecke den String, der als erstes Argument übergeben wurde in eine Variable
    excel_datei = sys.argv[1]
    return excel_datei

def get_kundennummer_und_zeitraum():
    excel_dateiname = get_excel_file_name()
    # Lese mit der Pandas-Instanz die Datei ein, und speicher den DataFrame in einer Variable
    df = pd.read_excel(excel_dateiname, engine="openpyxl", sheet_name="Tabelle1", header=None, skiprows=3, nrows=3, usecols="C")
    was_steht_da = df.values.tolist()
    return was_steht_da

def get_period_out_of_excel():
    excel_dateiname = get_excel_file_name()
    df = pd.read_excel(excel_dateiname, engine="openpyxl", sheet_name="Tabelle1", header=None, skiprows=11, usecols="A:E")

def get_time_data_out_of_excel():
    excel_dateiname = get_excel_file_name()
    df = pd.read_excel(excel_dateiname, engine="openpyxl", sheet_name="Tabelle1", header=None, skiprows=11, usecols="A:E")

    for i, row in df.iterrows():
        if row.isnull().all():
            df = df.iloc[:i]  # nur bis zur ersten leeren Zeile
            break
    
    data_dump = df.values.tolist()
    print(tabulate(data_dump))
    return data_dump


def get_kunden_daten():
    # Lies die Kundendaten aus der Kundentabelle anhand der Kundennummer
    Kundennummerliste = get_kundennummer_und_zeitraum()
    KundenNummer = Kundennummerliste[0][0]
    # Lies die Kundenliste ein
    df = pd.read_excel(KUNDENLISTE, engine="openpyxl")
    # Speichern der Zeile mit KndNr in einer Variablen
    Kunden_Zeile = df.loc[df['KndNr.'] == KundenNummer]
    liste_mit_einem_datensatz = Kunden_Zeile.values.tolist()
    print(tabulate(liste_mit_einem_datensatz))
    daten = liste_mit_einem_datensatz[0]
    return daten



if __name__ == "__main__":
    get_kunden_daten()
