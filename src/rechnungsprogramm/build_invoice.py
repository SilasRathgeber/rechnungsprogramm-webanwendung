from tabulate import tabulate
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from rechnungsprogramm.config import *
from rechnungsprogramm.get_data import get_kundennummer, get_excel_data
import pandas as pd
from reportlab.platypus import PageTemplate, Frame, Table
from reportlab.lib.pagesizes import A4
from rechnungsprogramm.build_template import zeichne_briefpapier

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


def erstelle_rechnung(daten, pfad="rechnung.pdf"):

    leftMargin = 25 * mm
    rightMargin = 20 * mm
    topMargin = 55 * mm
    bottomMargin = 55 * mm

    #width, height = A4

    doc = SimpleDocTemplate(pfad, pagesize=A4, leftMargin=leftMargin, rightMargin=rightMargin, topMargin=topMargin, bottomMargin=bottomMargin)

    #frame = Frame(leftMargin, bottomMargin, (width-leftMargin-rightMargin), (height-bottomMargin-topMargin), id='Inhalt')
    #template = PageTemplate(id='Briefpapier', frames=frame, onPage=zeichne_briefpapier)
    #doc.addPageTemplates([template])

    tabelle = Table(daten, colWidths=[15 * mm] * 7)
    flowables = [tabelle]

    doc.build(flowables, onFirstPage=zeichne_briefpapier, onLaterPages=zeichne_briefpapier)


def generate_invoice():

    print(tabulate(get_kunden_daten()))
    erstelle_rechnung(get_kunden_daten())


if __name__ == "__main__":
    generate_invoice()