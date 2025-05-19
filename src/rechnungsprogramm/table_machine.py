from reportlab.platypus import Table
from rechnungsprogramm.get_data import get_kunden_daten, get_time_content
from rechnungsprogramm.config import FRAMEWIDTH


def generate_invoice_head():
    spaltenanzahl = 7
    daten = get_kunden_daten()
    spaltenbreiten = [FRAMEWIDTH / spaltenanzahl] * spaltenanzahl
    tabelle = Table(daten, colWidths=spaltenbreiten)
    return tabelle 


def generate_invoice_content():
    spaltenanzahl = 5
    df = get_time_content()
    daten = [df.columns.tolist()] + df.values.tolist()
    spaltenbreiten = [FRAMEWIDTH / spaltenanzahl] * spaltenanzahl
    tabelle = Table(daten, colWidths=spaltenbreiten)
    return tabelle 
