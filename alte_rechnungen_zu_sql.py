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
        return "'NULL'"
    return f"'{val}'"

def clean_number_string(s: str) -> str:
    if not s or not s.strip():
        return "'NULL'"
    s = s.strip()
    match = re.search(r"[\d.,]+", s)
    if not match:
        return "'NULL'"
    num = match.group().replace(",", ".")
    try:
        return str(float(num))
    except ValueError:
        return "'NULL'"

def erste_zahl(s):
    match = re.search(r"\d+(?:[\.,]\d+)?", s)  # sucht ganze Zahl oder Kommazahl
    if match:
        return float(match.group().replace(",", "."))
    return float("inf")  # wenn keine Zahl gefunden, ganz nach hinten sortieren

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
    rechnungen_zeit_sql = []
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
            print(f"Rechnungsnummer zu {dateiname}: {rechnungsnummer}")
            kundennummer = data_dict.get("Kunden-Nr.")
            rechnungsdatum = data_dict.get("Rechnungsdatum")
            leistungszeitraum = data_dict.get("Leistungszeitraum")

            zeitraum = leistungszeitraum.replace("–", "-").replace("—", "-")
            von = sql_value(zeitraum.split("-")[0].strip())
            bis = sql_value(zeitraum.split("-")[1].strip())
            print(f"von: {von}| bis: {bis}|")
            
            rechnungen_sql.append(
                f"INSERT INTO rechnungen (id, kunde_id, re_datum, abrechnungsart, bezahlt) VALUES ("
                f"{rechnungsnummer}, "
                f"{kundennummer}, "
                f"'{rechnungsdatum}', "
                f"'zeit', "
                f"'1'"
                f");"
            )
            rechnungen_zeit_sql.append(
                f"INSERT INTO rechnungen_zeit (rechnung_id, zeitraum_von, zeitraum_bis) VALUES ("
                f"{rechnungsnummer}, "
                f"{von}, "
                f"{bis} "
                f");"    
            ) 
            zeiterfassungen_sql.append(f"INSERT INTO zeiterfassungen (id, kunde_id, rechnung_id, von, bis) VALUES (" \
                f"{zeiterfassung_id}, " \
                f"{kundennummer}, " \
                f"{rechnungsnummer}, " \
                f"{von}, " \
                f"{bis}, " \
                f"'zeitabrechnung');")   

            #print(data_dict)

        tabelle1 = eintrag['tables'][1]
        data = [['Bezeichnung', 'Datum', 'Start', 'Stop', 'Stunden', 'Stundensatz', 'Gesamt']]

        datum = None
        start_zeit = None
        stop_zeit = None
        zaehler = 0
        #try:
        for zeile in tabelle1[1:]:
            if len(zeile) < 4 or zeile[0] in ("", "Summe:", "/"):
                continue  # Überspringe ungültige Zeile

            zelle = zeile[0]
            teile = zelle.split('\n', 1)
            bezeichnung = teile[0].strip()
            datum = start_zeit = stop_zeit = None

            if len(zeile) == 5:
                bezeichnung = zeile[1].strip()
                datum = zeile[0]
                datum_sql = sql_value(datum)
                # Zahlen bereinigen
                stunden = clean_number_string(zeile[2])
                stundensatz = clean_number_string(zeile[3])
                gesamt = clean_number_string(zeile[4])
            else:
                if len(teile) == 2:
                    zeitinfo = teile[1].strip()

                    # Beispiel: "01.08.2025 08:00 - 12:00"
                    if " " in zeitinfo:
                        datum_part, zeiten = zeitinfo.split(" ", 1)
                        datum = datum_part.strip()
                        if "25 + 29.04.25" in zeitinfo:
                            datum="29.05.25"
                        zeiten = zeitinfo.split("+", 1)[0].strip()
                        zeiten = zeiten.replace("–", "-").replace("—", "-").replace("Uhr", "")
                        if "-" in zeiten:
                            start_zeit, stop_zeit = [t.strip() for t in zeiten.split("-", 1)]
                            start_zeit = start_zeit.split(" ")[1].strip()

                # SQL-Werte vorbereiten (ggf. auch None zulassen)
                datum_sql = sql_value(datum)
                start_sql = sql_value(start_zeit)
                stop_sql = sql_value(stop_zeit)

                # Zahlen bereinigen
                stunden = clean_number_string(zeile[1])
                stundensatz = clean_number_string(zeile[2])
                gesamt = clean_number_string(zeile[3])
                
            zeiteintraege_sql.append(f"INSERT INTO zeiteintraege (zeiterfassung_id, datum, startzeit, endzeit, beschreibung, stunden, stundensatz, gesamt) VALUES (" \
                f"{zeiterfassung_id}, " \
                f"{datum_sql}, " \
                f"{start_sql}, " \
                f"{stop_sql}, " \
                f"{sql_value(bezeichnung)}, " \
                f"{stunden}, " \
                f"{stundensatz}, "\
                f"{gesamt});")   

        # except IndexError as e:
        #     print(f"⚠️ Fehler in Datei '{dateiname}': Zeile unvollständig → {e}")
        # except Exception as e:
        #     print(f"❌ Allgemeiner Fehler in Datei '{dateiname}': {e}")

        zeiterfassung_id += 1

        rechnungen_sql = sorted(rechnungen_sql, key=erste_zahl)
    
    with open("daten_aus_rechnungen_import.sql", "w", encoding="utf-8") as f:
        for cmd in rechnungen_sql:
            f.write(cmd + "\n")
        for cmd in rechnungen_zeit_sql:
            f.write(cmd + "\n")
        for cmd in zeiterfassungen_sql:
            f.write(cmd + "\n")
        for cmd in zeiteintraege_sql:
            f.write(cmd + "\n")

if __name__ == "__main__":
    folder_route()


