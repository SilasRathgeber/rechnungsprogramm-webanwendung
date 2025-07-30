import sys
import pandas as pd

if len(sys.argv) != 2:
    print("Bitte eine Excel-Datei als Argument übergeben. (Endung .xlsx)")
    sys.exit()

excel_datei = sys.argv[1]
df = pd.read_excel(excel_datei, engine="openpyxl")

sql_commands= []

for index, row in df.iterrows():
    print(f"KndNr.: {row['KndNr.']}, Name: {row['Name']}, Straße: {row['Straße']}")

    sql_commands.append(f"INSERT INTO kunden (id, name, strasse, hausnummer, plz, ort, stundensatz) VALUES (" \
                  f"{row['KndNr.']}, " \
                  f"'{row['Name']}', " \
                  f"'{row['Straße']}', " \
                  f"'{row['Hausnummer']}', " \
                  f"'{row['Postleitzahl']}', " \
                  f"'{row['Ort']}', " \
                  f"{row['Vereinbarter Stundensatz']});")




    with open("kunden_import.sql", "w", encoding="utf-8") as f:
        for cmd in sql_commands:
            f.write(cmd + "\n")