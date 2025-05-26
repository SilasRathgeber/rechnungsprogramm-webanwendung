from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph
from reportlab.lib.units import mm
from rechnungsprogramm.config import *
from rechnungsprogramm.get_data import get_kunden_daten
from rechnungsprogramm.table_machine import generate_invoice_head, generate_invoice_content
from rechnungsprogramm.build_template import on_the_first_page, on_later_pages
from rechnungsprogramm.generate_pdf_name import generate_file_name

def erstelle_rechnung(datensatz_aus_kundenliste, datensatz_aus_zeitdatei, datensatz_mit_kdr_daten, rechnungsnummer):
    
    pfad = generate_file_name(rechnungsnummer)
    doc = SimpleDocTemplate(pfad, pagesize=A4, leftMargin=LEFTMARGIN, rightMargin=RIGHTMARGIN, topMargin=TOPMARGIN, bottomMargin=BOTTOMMARGIN)
    
    tabelle1 = generate_invoice_head(datensatz_aus_kundenliste, datensatz_mit_kdr_daten, rechnungsnummer)
    tabelle1.spaceBefore = 0
    tabelle1.spaceAfter = 0
    spacer1 = Spacer(1, 37 * mm)
    tabelle2 = generate_invoice_content(datensatz_aus_zeitdatei, datensatz_aus_kundenliste)
    styles = getSampleStyleSheet()
    text_unter_tabelle = ParagraphStyle(
        name="text_unter_tabelle",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName="Calibri",
        fontSize=11,
        textColor=HexColor("#000000"),
        spaceAfter=12,
        leading=25,
        alignment=0
    )
    para = Paragraph(f"Zahlbar ohne Abzüge innerhalb von 14 Tagen nach Erhalt der Rechnung<br/>Als Kleinunternehmer im Sinne von § 19 Abs. 1 UStG wird keine Umsatzsteuer berechnet.<br/>Ich bedanke mich für Ihren Auftrag und freue mich auf die weitere Zusammenarbeit.", text_unter_tabelle)
    spacer2 = Spacer(1, 10 * mm)
    flowables = [tabelle1, spacer1, tabelle2, spacer2, para]
    doc.build(flowables, onFirstPage=on_the_first_page, onLaterPages=on_later_pages)


if __name__ == "__main__":
    erstelle_rechnung()