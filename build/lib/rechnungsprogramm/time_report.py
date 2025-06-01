from tabulate import tabulate
import pandas

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
        

    def print_time_report(self):
        data_head = [[
            self.kundennummer,
            self.start_day,
            self.stop_day,
        ]]
        data_content = self.content
        
        print(tabulate(data_head, tablefmt="fancy_grid"))
        print(tabulate(data_content, tablefmt="rst"))