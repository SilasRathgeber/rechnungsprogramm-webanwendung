
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph
from reportlab.lib.units import mm
from rechnungsprogramm.config import *
from rechnungsprogramm.get_data import get_kunden_daten
from rechnungsprogramm.table_machine import generate_invoice_head, generate_invoice_content
from rechnungsprogramm.build_template import on_the_first_page, on_later_pages

def erstelle_rechnung(datensatz_aus_kundenliste, datensatz_aus_zeitdatei, datensatz_mit_kdr_daten, pfad="rechnung.pdf"):

    doc = SimpleDocTemplate(pfad, pagesize=A4, leftMargin=LEFTMARGIN, rightMargin=RIGHTMARGIN, topMargin=TOPMARGIN, bottomMargin=BOTTOMMARGIN)
    
    tabelle1 = generate_invoice_head(datensatz_aus_kundenliste, datensatz_mit_kdr_daten)
    tabelle1.spaceBefore = 0
    tabelle1.spaceAfter = 0
    spacer1 = Spacer(1, 50 * mm)
    tabelle2 = generate_invoice_content(datensatz_aus_zeitdatei, datensatz_aus_kundenliste)
    flowables = [tabelle1, spacer1, tabelle2]
    doc.build(flowables, onFirstPage=on_the_first_page, onLaterPages=on_later_pages)


if __name__ == "__main__":
    erstelle_rechnung()