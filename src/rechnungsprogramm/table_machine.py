from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from datetime import datetime
from rechnungsprogramm.config import FRAMEWIDTH, FIRMEN_ADRESSE_ORT, FIRMEN_ADRESSE_STRASSE, FIRMEN_NAME
from tabulate import tabulate

def generate_invoice_head(kundendaten_gelistet: list, datensatz_mit_kdr_daten: list) -> None:
    heute = datetime.now()
    deutsches_datum = heute.strftime("%d.%m.%Y")
    STARTDATUMlst = datensatz_mit_kdr_daten[1][0]
    ENDDATUMlst = datensatz_mit_kdr_daten[2][0]
    STARTDATUM = STARTDATUMlst.strftime("%d.%m.%Y")
    ENDDATUM = ENDDATUMlst.strftime("%d.%m.%Y")
    KUNDENNR, KUNDENNAME, KUNDENSTRASSE, KUNDENHSNR, KUNDENPLZ, KUNDENORT, KUNDENSTDSATZ = kundendaten_gelistet
    styles = getSampleStyleSheet()

    absender_style = ParagraphStyle(
        name="absender_style",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName="Calibri",
        fontSize=8,
        textColor=HexColor("#000000"),
        spaceAfter=12,
        leading=8
    )
    aempfaenger_style = ParagraphStyle(
        name="aempfaenger_style",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName="Calibri",
        fontSize=11,
        textColor=HexColor("#000000"),
        #spaceAfter=12,
        leading=11
    )
    invoice_head_style = ParagraphStyle(
        name="invoice_head_style",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName="Calibri",
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
        Paragraph(f">Rechnungsnummer<<br/>{KUNDENNR}<br/>{deutsches_datum}<br/>{STARTDATUM} - {ENDDATUM}", invoice_head_style)
        ]

    tabelle = Table(tabellen_struktur, colWidths=[85 * mm, 45 * mm, 45 * mm], rowHeights=[15 * mm, 30 *mm])
    tabelle.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (0,1), colors.HexColor('#F2F2F2')),
    ('VALIGN', (0,0), (0,1), 'TOP')
    ]))
    return tabelle 


def generate_invoice_content(viele_zeilen, kundendaten: list):


    styles = getSampleStyleSheet()
    ueberschriften = ParagraphStyle(
        name="ueberschriften",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName="CalibriB",
        fontSize=11,
        textColor=HexColor("#000000"),
        spaceAfter=12,
        leading=11
    )
    
    spaltenanzahl = 4
    spaltenbreiten = [FRAMEWIDTH / spaltenanzahl] * spaltenanzahl
    
    tabellen_struktur = [
        Paragraph(f"Bezeichnung", ueberschriften),
        Paragraph(f"Stunden", ueberschriften),
        Paragraph(f"€/h", ueberschriften),
        " ",
        ], [
        Paragraph(f"",), 
        f"\n", 
        f"\n",
        " "
        ], [
        Paragraph(f"", ), 
        Paragraph(f"", ), 
        Paragraph(f"", )
        ]
    
    tabelle = Table(tabellen_struktur, colWidths=spaltenbreiten)
    tabelle.setStyle(TableStyle([
    ('LINEBELOW', (0,0), (-1,0), 1, colors.black),
    ('VALIGN', (0,0), (-1,0), 'MIDDLE')
    #('BACKGROUND', (0,0), (0,-1), colors.lightblue),
    ]))
    return tabelle 
