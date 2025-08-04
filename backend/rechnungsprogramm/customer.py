import pandas
from tabulate import tabulate
from backend.config import db_path
import sqlite3

class Customer:
    def __init__(self, customer_id, name, street, house_number, postal_code, city, fee):
        self.customer_id = customer_id
        self.name = name
        self.street = street
        self.house_number = house_number
        self.postal_code = postal_code
        self.city = city
        self.fee = fee

    @classmethod
    def from_excel(cls, kundenliste_path: str, kundennummer: str):
        df = pandas.read_excel(kundenliste_path, engine="openpyxl")
        row = df.loc[df['KndNr.'] == kundennummer].iloc[0]
        return cls(
            customer_id=row['KndNr.'],
            name=row['Name'],
            street=row['Straße'],
            house_number = row['Hausnummer'],
            postal_code=row['Postleitzahl'],
            city=row['Ort'],
            fee=row['Vereinbarter Stundensatz']
            )
    
    @classmethod
    def from_sqlite(cls, zeiterfassungs_id: int):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT k.id, k.name, k.strasse, k.hausnummer, k.plz, k.ort, k.stundensatz
                FROM kunden k
                JOIN zeiterfassungen z ON z.kunde_id = k.id
                WHERE z.id = ?
            """, (zeiterfassungs_id,))
            row = cursor.fetchone()
            if row is None:
                raise ValueError(f"Kein Kunde für Zeiterfassungs-ID {zeiterfassungs_id} gefunden.")
            return cls(
                customer_id=row[0],
                name=row[1],
                street=row[2],
                house_number=row[3],
                postal_code=row[4],
                city=row[5],
                fee=row[6]
            )

    def print_tabulated(self):
        data = [[
            self.customer_id,
            self.name,
            self.street,
            self.house_number,
            self.postal_code,
            self.city,
            self.fee
        ]]
        print(tabulate(data, tablefmt="fancy_grid"))