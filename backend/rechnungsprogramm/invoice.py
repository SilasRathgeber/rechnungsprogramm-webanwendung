from datetime import datetime, date
from reportlab.platypus import Paragraph
from decimal import Decimal, ROUND_HALF_UP
from rechnungsprogramm.customer import Customer
from rechnungsprogramm.time_report import TimeReport

class Invoice:
    def __init__(self, customer: Customer, time_report: TimeReport):
        self.customer = customer
        self.time_report = time_report
        self.total_hours = Decimal(0.0)
        self.total_price = Decimal(0.0)
        self.invoice_items = 0

    def raise_data_item_table(self):
        tabelle = []

        for i, unterliste in enumerate(self.time_report.content):
                TAGESDATUM = None
                BESCHREIBUNG = None
                START = None
                STOP = None
                for j, element in enumerate(unterliste):
                    if j==0:
                        if isinstance(element, str):
                            element = datetime.strptime(element, "%y-%m-%d")
                        TAGESDATUM = element.strftime("%d.%m.%Y")
                    if j==2:
                        BESCHREIBUNG = element
                    if j==3:
                        START = element
                    if j==4:
                        STOP = element
                self.invoice_items += 1
                start_dt = datetime.combine(date.today(), START)
                stop_dt = datetime.combine(date.today(), STOP)
                dauer = stop_dt - start_dt
                dauer_stunden = Decimal(str(dauer.total_seconds() / 3600))
                satz = Decimal(str(self.customer.fee))
                stunden_mal_satz = (satz * dauer_stunden).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                anzeige_start = START.strftime("%H:%M")
                anzeige_stop = STOP.strftime("%H:%M")
                self.total_price += stunden_mal_satz
                self.total_hours += dauer_stunden

                zeile = [
                    f"{BESCHREIBUNG}<br/><font color=#A6A6A6 size=8>{TAGESDATUM} {anzeige_start} - {anzeige_stop} Uhr</font>",
                    f"{dauer_stunden}".replace(".",","),
                    f"{self.customer.fee}",
                    f"{stunden_mal_satz:.2f} €".replace(".",",")
                ]
                tabelle.append(zeile)
        print(f"STUNDEN GESAMT: {self.total_hours}")
        return tabelle