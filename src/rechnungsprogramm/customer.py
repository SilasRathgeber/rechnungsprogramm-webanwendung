import pandas
from tabulate import tabulate

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