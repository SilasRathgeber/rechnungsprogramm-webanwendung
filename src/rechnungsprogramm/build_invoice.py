
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.units import mm
from rechnungsprogramm.config import *
from rechnungsprogramm.table_machine import generate_invoice_head, generate_invoice_content
import pandas as pd

from rechnungsprogramm.build_template import zeichne_briefpapier

def erstelle_rechnung(daten, pfad="rechnung.pdf"):

    doc = SimpleDocTemplate(pfad, pagesize=A4, leftMargin=LEFTMARGIN, rightMargin=RIGHTMARGIN, topMargin=TOPMARGIN, bottomMargin=BOTTOMMARGIN)

    tabelle1 = generate_invoice_head()
    tabelle2 = generate_invoice_content()
    flowables = [tabelle1, tabelle2]
    doc.build(flowables, onFirstPage=zeichne_briefpapier, onLaterPages=zeichne_briefpapier)


if __name__ == "__main__":
    erstelle_rechnung()