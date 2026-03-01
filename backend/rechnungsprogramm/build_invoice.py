import os
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Spacer, Paragraph
from reportlab.lib.units import mm
from .config import *
from .table_machine import generate_invoice_head, generate_invoice_content
from .build_template import on_the_first_page, on_later_pages
from .generate_pdf_name import generate_file_name
from .customer import Customer
from .find_speicherpfad import find_pfad
from .numbered_canvas_class import *

def erstelle_rechnung(vorschau: int, kunde: Customer, rechnung, report_head_infos, rechnungsnummer, standard_schriftart, font_table_head):
    
    if vorschau == 1:
        pfad = VORSCHAU_PFAD
        datei_name = os.path.basename(pfad)  # extrahiert "Vorschaudatei.pdf" aus dem Pfad
        os.makedirs(os.path.dirname(pfad), exist_ok=True)
    else:    
        datei_name = generate_file_name(rechnungsnummer, report_head_infos)
        base_pfad = find_pfad(rechnung.rechnungsdatum)
        pfad = f"{base_pfad}/{datei_name}"

    doc = SimpleDocTemplate(pfad, pagesize=A4, leftMargin=LEFTMARGIN, rightMargin=RIGHTMARGIN, topMargin=TOPMARGIN, bottomMargin=BOTTOMMARGIN)
    
    tabelle1 = generate_invoice_head(kunde, report_head_infos, rechnungsnummer, standard_schriftart, rechnung)
    tabelle1.spaceBefore = 0
    tabelle1.spaceAfter = 0
    spacer1 = Spacer(1, 37 * mm)
    tabelle2 = generate_invoice_content(rechnung, kunde, standard_schriftart, font_table_head)
    styles = getSampleStyleSheet()
    text_unter_tabelle = ParagraphStyle(
        name="text_unter_tabelle",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName=standard_schriftart,
        fontSize=11,
        textColor=HexColor("#000000"),
        spaceAfter=12,
        leading=25,
        alignment=0
    )
    para = Paragraph(f"Zahlbar ohne Abzüge innerhalb von 14 Tagen nach Erhalt der Rechnung<br/>Als Kleinunternehmer im Sinne von § 19 Abs. 1 UStG wird keine Umsatzsteuer berechnet.<br/>Ich bedanke mich für Ihren Auftrag und freue mich auf die weitere Zusammenarbeit.", text_unter_tabelle)
    spacer2 = Spacer(1, 10 * mm)
    flowables = [tabelle1, spacer1, tabelle2, spacer2, para]
    doc.build(flowables, onFirstPage=on_the_first_page, onLaterPages=on_later_pages, canvasmaker=NumberedCanvas)


    return datei_name, pfad

if __name__ == "__main__":
    erstelle_rechnung()