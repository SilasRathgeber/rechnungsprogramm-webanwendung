import os
from docx import Document
import pprint
import json
import re
from tabulate import tabulate

def extract_table_from_docx(file_path):
    doc = Document(file_path)
    tables_data = []

    for table in doc.tables:
        table_content = []
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells]
            table_content.append(cells)
        tables_data.append(table_content)

    return tables_data

def read_tables_from_folder(folder_path):
    all_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith(".docx"):
            path = os.path.join(folder_path, filename)
            tables = extract_table_from_docx(path)
            all_data.append({
                "filename": filename,
                "tables": tables
            })
    return all_data

def sql_value(val):
    if val is None or val.strip() == "":
        return "NULL"
    return f"'{val}'"

def folder_route():
    folder_list=[]
    folder_list.append("C:/Users/silas/OneDrive - Silas Rathgeber IT/Eigene Dokumente/Kleingewerbe - Silas Rathgeber IT-Dienstleistungen/Ausgangsrechnungen/2020")
    folder_list.append("C:/Users/silas/OneDrive - Silas Rathgeber IT/Eigene Dokumente/Kleingewerbe - Silas Rathgeber IT-Dienstleistungen/Ausgangsrechnungen/2021")
    folder_list.append("C:/Users/silas/OneDrive - Silas Rathgeber IT/Eigene Dokumente/Kleingewerbe - Silas Rathgeber IT-Dienstleistungen/Ausgangsrechnungen/2022")
    folder_list.append("C:/Users/silas/OneDrive - Silas Rathgeber IT/Eigene Dokumente/Kleingewerbe - Silas Rathgeber IT-Dienstleistungen/Ausgangsrechnungen/2023")
    folder_list.append("C:/Users/silas/OneDrive - Silas Rathgeber IT/Eigene Dokumente/Kleingewerbe - Silas Rathgeber IT-Dienstleistungen/Ausgangsrechnungen/2024")
    folder_list.append("C:/Users/silas/OneDrive - Silas Rathgeber IT/Eigene Dokumente/Kleingewerbe - Silas Rathgeber IT-Dienstleistungen/Ausgangsrechnungen/2025")
    all_entries = []
    zeiteintraege_sql = []
    rechnungen_sql = []
    zeiterfassungen_sql = []
    zeiterfassung_id = 3

    for item in folder_list:
        data = read_tables_from_folder(item)
        all_entries.extend(data)

    for eintrag in all_entries:
        dateiname = eintrag['filename']
        print(f"DATEI: {eintrag['filename']}")

        tabelle0 = eintrag['tables'][0]
        if len(tabelle0) > 0 and len(tabelle0[0]) >= 3:
            beschriftungen = tabelle0[0][1].split("\n")
            werte = tabelle0[0][2].split("\n")
            
            data_dict = dict(zip(beschriftungen, werte))

            rechnungsnummer = data_dict.get("Rechnungs-Nr.")
            kundennummer = data_dict.get("Kunden-Nr.")
            rechnungsdatum = data_dict.get("Rechnungsdatum")
            leistungszeitraum = data_dict.get("Leistungszeitraum")
            
            rechnungen_sql.append(
                f"INSERT INTO rechnungen (id, kunde_id, re_datum, zeitraum, projekt) VALUES ("
                f"{rechnungsnummer}, "
                f"{kundennummer}, "
                f"'{rechnungsdatum}', "
                f"'{leistungszeitraum}', "
                f"''"
                f");"
            )
            #print(data_dict)

        tabelle1 = eintrag['tables'][1]
        data = [['Bezeichnung', 'Datum', 'Start', 'Stop', 'Stunden', 'Stundensatz', 'Gesamt']]

        datum = None
        start_zeit = None
        stop_zeit = None
        zaehler = 0
        try:
            for zeile in tabelle1[1:]:
                if len(zeile) >= 4 and zeile[0] != "":

                    zelle = zeile[0]
                    teile = zelle.split('\n')
                    if len(teile) >= 2:
                        bezeichnung = teile[0]
                        zeitangabe_teile = teile[1].split(' ', 1)
                        if len(zeitangabe_teile) == 2:
                            datum = zeitangabe_teile[0]
                            zeiten_teile = zeitangabe_teile[1].replace('–', '-').replace('—', '-').split('-', 1)
                            if len(zeiten_teile) == 2:
                                start_zeit = zeiten_teile[0].strip()
                                stop_zeit = zeiten_teile[1].strip()
                                start_sql = sql_value(start_zeit)
                                stop_sql = sql_value(stop_zeit)
                            else:
                                start_sql = sql_value(start_zeit)
                                stop_sql = sql_value(stop_zeit)
                        else:
                            datum_sql = sql_value(datum)
                            start_sql = sql_value(start_zeit)
                            stop_sql = sql_value(stop_zeit)
                    else:
                        bezeichnung = teile[0]
                        datum_sql = sql_value(datum)
                        start_sql = sql_value(start_zeit)
                        stop_sql = sql_value(stop_zeit)
                    stunden = zeile[1]
                    stundensatz = zeile[2]
                    gesamt = zeile[3]

                    zeile = [bezeichnung, datum, start_zeit, stop_zeit, stunden , stundensatz, gesamt]
                    data.append(zeile)  
                     
                    zeiterfassungen_sql.append(f"INSERT INTO zeiterfassungen (id, kunde_id, rechnung_id, typ) VALUES (" \
                        f"{zeiterfassung_id}, " \
                        f"{kundennummer}, " \
                        f"{rechnungsnummer}, " \
                        f"'zeitabrechnung');")   

                    zeiterfassung_id += 1

                    zeiteintraege_sql.append(f"INSERT INTO zeiteintraege (zeiterfassung_id, datum, startzeit, endzeit, beschreibung) VALUES (" \
                        f"{zeiterfassung_id}, " \
                        f"{datum_sql}, " \
                        f"{start_sql}, " \
                        f"{stop_sql}, " \
                        f"{sql_value(bezeichnung)});")   
 
            #print(tabulate(data, headers="firstrow", tablefmt="grid"))
        except IndexError as e:
            print(f"⚠️ Fehler in Datei '{dateiname}': Zeile unvollständig → {e}")
        except Exception as e:
            print(f"❌ Allgemeiner Fehler in Datei '{dateiname}': {e}")

    with open("daten_aus_rechnungen_import.sql", "w", encoding="utf-8") as f:
        for cmd in rechnungen_sql:
            f.write(cmd + "\n")
        for cmd in zeiterfassungen_sql:
            f.write(cmd + "\n")
        for cmd in zeiteintraege_sql:
            f.write(cmd + "\n")

if __name__ == "__main__":
    folder_route()


