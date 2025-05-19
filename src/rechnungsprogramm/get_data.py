import pandas as pd
import sys
from rechnungsprogramm.config import KDNRX, KDNRY, DATA_DIR


def get_excel_file_name():
    if len(sys.argv) != 2:
        print("Bitte eine Excel-Datei als Argument übergeben. (Endung .xlsx)")
        sys.exit()
    # Stecke den String, der als erstes Argument übergeben wurde in eine Variable
    excel_datei = sys.argv[1]
    return excel_datei

def get_excel_data():
    excel_dateiname = get_excel_file_name()
    # Lese mit der Pandas-Instanz die Datei ein, und speicher den DataFrame in einer Variable
    df = pd.read_excel(excel_dateiname, engine="openpyxl")
    return df

def get_kundennummer(df):
    # Nimm aus dem gespeicherten DataFrame nur eine bestimmte Zelle und speicher sie
    KundenNummer = df.iloc[KDNRX, KDNRY]
    return(KundenNummer)

def get_data_table(df):
    table = df.iloc[0:12, 4:28]
    return table

def get_kunden_daten():
    # Lies die Kundendaten aus der Kundentabelle anhand der Kundennummer
    KundenNummer = get_kundennummer(get_excel_data())

    # Lies die Kundenliste ein
    df = pd.read_excel(DATA_DIR/"Liste_Kunden.xlsx", engine="openpyxl")

    # Speichern der Zeile mit KndNr in einer Variablen
    Kunden_Zeile = df.loc[df['KndNr.'] == KundenNummer]
    kopf = list(Kunden_Zeile.columns)
    daten = Kunden_Zeile.values.tolist()
    return [kopf] + daten

def get_time_content():
    daten = get_data_table(get_excel_data())
    return daten

if __name__ == "__main__":
    get_excel_data()
