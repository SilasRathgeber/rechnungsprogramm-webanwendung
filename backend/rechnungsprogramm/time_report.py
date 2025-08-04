from tabulate import tabulate
import pandas
from backend.config import db_path
import sqlite3
from datetime import datetime



class TimeReport:
    def __init__(self, kundennummer, start_day, stop_day, content: list):
        self.kundennummer = kundennummer
        self.start_day = start_day
        self.stop_day = stop_day
        self.content = content

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
                    SELECT kunde_id, von, bis
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
                    if t is None or t == '':
                        return None
                    try:
                        return datetime.strptime(t, "%H:%M").time()  # Format anpassen, je nach DB
                    except ValueError:
                        raise ValueError(f"Ungültige Zeit: {t}")

                start = parse_time(start_str)
                stop = parse_time(stop_str)

                content.append([datum, None, beschreibung, start, stop])


            kundennummer, start_day_str, stop_day_str = zeiterfassung_row

            start_day = datetime.strptime(start_day_str, "%Y-%m-%d")
            stop_day = datetime.strptime(stop_day_str, "%Y-%m-%d")

        return cls(
            kundennummer=kundennummer,
            start_day=start_day,
            stop_day=stop_day,
            content=content
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