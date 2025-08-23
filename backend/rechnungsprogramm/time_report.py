from tabulate import tabulate
import pandas
from backend.config import db_path
import sqlite3
from datetime import datetime



class TimeReport:
    def __init__(self, kundennummer, start_day, stop_day, content: list, stundensatz):
        self.kundennummer = kundennummer
        self.start_day = start_day
        self.stop_day = stop_day
        self.content = content
        self.stundensatz = stundensatz

    @classmethod
    def from_excel(cls, time_report_path: str):
        df_head = pandas.read_excel(time_report_path, engine="openpyxl", sheet_name="Tabelle1", header=None, skiprows=3, nrows=3, usecols="C")
        df_content = pandas.read_excel(time_report_path, engine="openpyxl", sheet_name="Tabelle1", header=None, skiprows=11, usecols="A:E")

        for i, row in df_content.iterrows():
            if row.isnull().all():
                df_content = df_content.iloc[:i]  # nur bis zur ersten leeren Zeile
                break
        
        return cls(
            kundennummer = df_head.iloc[0, 0],
            start_day = df_head.iloc[1, 0],
            stop_day = df_head.iloc[2, 0],
            content = df_content.values.tolist()
            )
    
    @classmethod
    def from_sql(cls, zeiterfassungs_id: int):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                    SELECT kunde_id, von, bis, stundensatz
                    FROM zeiterfassungen 
                    WHERE id = ?
                """, (zeiterfassungs_id,))
            zeiterfassung_row = cursor.fetchone()
            if zeiterfassung_row is None:
                    raise ValueError(f"Kein Kunde für Zeiterfassungs-ID {zeiterfassungs_id} gefunden.")

            cursor.execute("""
                    SELECT datum, beschreibung, startzeit, endzeit
                    FROM zeiteintraege
                    WHERE zeiterfassung_id = ?
                    ORDER BY datum
                """, (zeiterfassungs_id,))
            
            rows = cursor.fetchall()
            content = []

            for row in rows:
                datum_str, beschreibung, start_str, stop_str = row

                # Datum ggf. in datetime-Objekt umwandeln
                try:
                    datum = datetime.strptime(datum_str, "%Y-%m-%d")
                except ValueError:
                    datum = datum_str  # oder Exception werfen

                # Startzeit und Endzeit in time-Objekte umwandeln, falls nicht None oder leer
                def parse_time(t):
                    if t is None or t == '' or t.upper() == 'NULL':
                        return None
                    try:
                        return datetime.strptime(t, "%H:%M").time()  # Format anpassen, je nach DB
                    except ValueError:
                        raise ValueError(f"Ungültige Zeit: {t}")

                start = parse_time(start_str)
                stop = parse_time(stop_str)

                content.append([datum, None, beschreibung, start, stop])


            kundennummer, start_day_str, stop_day_str, stundensatz = zeiterfassung_row
            

            cursor.execute("""
            SELECT k.aktueller_stundensatz
            FROM zeiterfassungen z
            JOIN kunden k ON z.kunde_id = k.id
            WHERE z.id = ?;
            """, (zeiterfassungs_id,))
            row = cursor.fetchone()
            aktueller_stundensatz = float(row[0]) if row and row[0] is not None else 0.0

            
            if stundensatz in ('', 'NULL', None) and aktueller_stundensatz not in ('', 'NULL', None):
                print("Hallo aus if stundensatz ist Null aber aktueller_stundensatz ist nicht Null")
                # Wenn in stundensatz von zeiterfassungen nichts drinnen steht, nimm den Stundensatz aus der kundentabelle aus "aktueller_stundensatz"
                stundensatz = aktueller_stundensatz
                cursor.execute("""
                UPDATE zeiterfassungen
                SET stundensatz = ?
                WHERE id = ?
                """, (aktueller_stundensatz, zeiterfassungs_id))
                conn.commit()
            elif stundensatz not in (None, '', 'NULL', '0.0') and stundensatz != 0.0 and aktueller_stundensatz != stundensatz:
                print("Hallo aus stundensatz ist nicht null und aktueller_stundensatz ist nicht gleich stundensatz")
                print("stundensatz aus zeiterfassung:", stundensatz)
                print("aktueller_stundensatz aus kunde:", aktueller_stundensatz)
                cursor.execute("""
                UPDATE kunden
                SET aktueller_stundensatz = ?
                WHERE id = (
                    SELECT kunde_id
                    FROM zeiterfassungen
                    WHERE id = ?
                );
                """, (stundensatz, zeiterfassungs_id))

                conn.commit()

            
            

            stundensatz = float(row[0]) if row and row[0] is not None else 0.0
            start_day = datetime.strptime(start_day_str, "%Y-%m-%d")
            stop_day = datetime.strptime(stop_day_str, "%Y-%m-%d")

        return cls(
            kundennummer=kundennummer,
            start_day=start_day,
            stop_day=stop_day,
            content=content,
            stundensatz=stundensatz
        )

    def print_time_report(self):
        data_head = [[
            self.kundennummer,
            self.start_day,
            self.stop_day,
        ]]
        data_content = self.content
        
        print(tabulate(data_head, tablefmt="fancy_grid"))
        print(tabulate(data_content, tablefmt="rst"))