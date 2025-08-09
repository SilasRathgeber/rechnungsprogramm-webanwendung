from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from datetime import datetime, date
from .config import FRAMEWIDTH, FIRMEN_ADRESSE_ORT, FIRMEN_ADRESSE_STRASSE, FIRMEN_NAME
from .generate_rechnungsnummer import generate_rechnungsnummer
from .customer import Customer
from .invoice import Invoice

def generate_invoice_head(kunde: Customer, report_head_infos: list, rechnungsnummer, standard_schriftart) -> None:
    heute = datetime.now()
    deutsches_datum = heute.strftime("%d.%m.%Y")
    STARTDATUMlst = report_head_infos[1]
    ENDDATUMlst = report_head_infos[2]

    STARTDATUM = STARTDATUMlst.strftime("%d.%m.%Y")
    ENDDATUM = ENDDATUMlst.strftime("%d.%m.%Y")

    KUNDENNR = kunde.customer_id
    KUNDENNAME = kunde.name
    KUNDENSTRASSE = kunde.street
    KUNDENHSNR = kunde.house_number
    KUNDENPLZ = kunde.postal_code
    KUNDENORT = kunde.city

    styles = getSampleStyleSheet()

    absender_style = ParagraphStyle(
        name="absender_style",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName=standard_schriftart,
        fontSize=8,
        textColor=HexColor("#000000"),
        #spaceAfter=12,
        leading=8
    )
    aempfaenger_style = ParagraphStyle(
        name="aempfaenger_style",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName=standard_schriftart,
        fontSize=11,
        textColor=HexColor("#000000"),
        #spaceAfter=12,
        leading=11
    )
    invoice_head_style = ParagraphStyle(
        name="invoice_head_style",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName=standard_schriftart,
        fontSize=11,
        textColor=HexColor("#000000"),
        #spaceAfter=12,
        leading=11,
        alignment=TA_RIGHT
    )
    
    tabellen_struktur = [
        Paragraph(f"<br/>{FIRMEN_NAME} - {FIRMEN_ADRESSE_STRASSE} - {FIRMEN_ADRESSE_ORT}", absender_style), 
        f"\n", 
        f"\n"  
        ], [
        Paragraph(f"{KUNDENNAME}<br/>{KUNDENSTRASSE} {KUNDENHSNR}<br/>{KUNDENPLZ} {KUNDENORT}", aempfaenger_style), 
        Paragraph(f"Rechnungs-Nr.<br/>Kunden-Nr.<br/>Rechnungsdatum<br/>Leistungszeitraum", invoice_head_style), 
        Paragraph(f"{rechnungsnummer}<br/>{KUNDENNR}<br/>{deutsches_datum}<br/>{STARTDATUM} - {ENDDATUM}", invoice_head_style)
        ]

    col3 = 45 * mm
    col1 = 85 * mm # DIN norm Adressfeldbreite
    col2 = FRAMEWIDTH - col1 - col3
    tabelle = Table(tabellen_struktur, colWidths=[col1, col2, col3], rowHeights=[15 * mm, 30 *mm])
    tabelle.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,1), colors.HexColor('#F2F2F2')),
    ('VALIGN', (0,0), (0,1), 'TOP'),
    ('TOPPADDING', (0,0), (0,0), -1.00 * mm),
    ('LEFTPADDING', (0,0), (0,1), 3.21 * mm),  
    #("BOX", (0,0), (-1,-1), 1, colors.red),
    ]))
    return tabelle 


def generate_invoice_content(rechnung: Invoice, kunde: Customer, standard_schriftart, font_table_head):

    STUNDENSATZ = kunde.fee

    styles = getSampleStyleSheet()
    ueberschriften_rechts = ParagraphStyle(
        name="ueberschriften_rechts",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName=font_table_head,
        fontSize=11,
        textColor=HexColor("#000000"),
        spaceAfter=12,
        leading=11,
        alignment=2
    )
    ueberschriften_links = ParagraphStyle(
        name="ueberschriften_links",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName=font_table_head,
        fontSize=11,
        textColor=HexColor("#000000"),
        spaceAfter=12,
        leading=11,
        alignment=0
    )
    data_content = ParagraphStyle(
        name="data_content",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName=standard_schriftart,
        fontSize=11,
        textColor=HexColor("#000000"),
        spaceAfter=12,
        leading=11,
        alignment=2
    )
    style_beschreibung = ParagraphStyle(
        name="style_beschreibung",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName=standard_schriftart,
        fontSize=11,
        textColor=HexColor("#000000"),
        spaceAfter=12,
        leading=12,
        alignment=0
    )

    tabellen_struktur = [
         [
        Paragraph(f"Bezeichnung", ueberschriften_links),
        Paragraph(f"Stunden", ueberschriften_rechts),
        Paragraph(f"€/h", ueberschriften_rechts),
        Paragraph(f"Gesamt", ueberschriften_rechts),
         ]
    ] 

    table_content_raw = rechnung.raise_data_item_table()

    for i, unterliste in enumerate(table_content_raw):
        zeile = [
            Paragraph(table_content_raw[i][0], style_beschreibung), 
            Paragraph(table_content_raw[i][1], data_content), 
            Paragraph(table_content_raw[i][2], data_content),
            Paragraph(table_content_raw[i][3], data_content)
        ]
        tabellen_struktur.append(zeile)

    letzte_zeile = [
         "", 
         "",
         Paragraph(f"Gesamtbetrag:", data_content),
         Paragraph(f"{rechnung.total_price:.2f} €".replace(".",","), data_content)
    ]
    geister_zeile = [
         "","","",""
    ]

    tabellen_struktur.append(letzte_zeile)
    tabellen_struktur.append(geister_zeile)
    row_heights = []
    for zeile in tabellen_struktur:
         if zeile == ["","","",""]:
              row_heights.append(2)
         else:
              row_heights.append(None)
    col4 = 27.5 * mm
    col3 = 29.5 * mm
    col2 = 27.5 * mm
    col1 = FRAMEWIDTH - col2 - col3 - col4
    tabelle = Table(tabellen_struktur, colWidths=[col1, col2, col3, col4], rowHeights=row_heights)
    tabelle.setStyle(TableStyle([
    ('TOPPADDING', (0,0), (-1,-1), 2.21 * mm),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2.21 * mm),   
    ('LINEBELOW', (0,0), (-1,rechnung.invoice_items), 0.5, colors.black),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ('LINEBELOW', (2,rechnung.invoice_items+1), (3,rechnung.invoice_items+1), 0.5, colors.black),
    ('LINEBELOW', (2,rechnung.invoice_items+2), (3,rechnung.invoice_items+2), 0.5, colors.black),
    ]))
    return tabelle 
