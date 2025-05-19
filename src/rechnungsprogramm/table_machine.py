from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib import colors
from datetime import datetime
from rechnungsprogramm.get_data import get_kunden_daten, get_time_content
from rechnungsprogramm.config import FRAMEWIDTH, FIRMEN_ADRESSE_ORT, FIRMEN_ADRESSE_STRASSE, FIRMEN_NAME


def generate_invoice_head():
    #spaltenanzahl = 3
    heute = datetime.now()
    deutsches_datum = heute.strftime("%d.%m.%Y")
    daten = get_kunden_daten()
    einzelne_zeile = daten[0]
    KUNDENNR, KUNDENNAME, KUNDENSTRASSE, KUNDENHSNR, KUNDENPLZ, KUNDENORT, KUNDENSTDSATZ = einzelne_zeile
    styles = getSampleStyleSheet()
    styleN = styles['Normal']
    
    tabellen_struktur = [
        Paragraph(f"{FIRMEN_NAME} - {FIRMEN_ADRESSE_STRASSE} - {FIRMEN_ADRESSE_ORT}", styleN), f"\n", f"\n"  
        ], [
        f"{KUNDENNAME}\n{KUNDENSTRASSE} {KUNDENHSNR}\n{KUNDENPLZ} {KUNDENORT}", 
        f"Rechnungs-Nr.\n Kunden-Nr.\nRechnungsdatum\nLeistungszeitraum", 
        f">Rechnungsnummer<\n{KUNDENNR}\n{deutsches_datum}\n>Leistungszeitraum<"
        ]

    #spaltenbreiten = [FRAMEWIDTH / spaltenanzahl] * spaltenanzahl
    tabelle = Table(tabellen_struktur, colWidths=[85 * mm, 45 * mm, 45 * mm])
    tabelle.setStyle(TableStyle([
    #('GRID', (0,0), (-1,-1), 1, colors.black),
    ('BACKGROUND', (0,0), (0,1), colors.HexColor('#F2F2F2')),
    ('ALIGN', (1,0), (2,0), 'RIGHT')
    ]))
    return tabelle 


def generate_invoice_content():
    spaltenanzahl = 6
    df = get_time_content()
    daten = [df.columns.tolist()] + df.values.tolist()
    spaltenbreiten = [FRAMEWIDTH / spaltenanzahl] * spaltenanzahl
    tabelle = Table(daten, colWidths=spaltenbreiten)
    tabelle.setStyle(TableStyle([
    ('GRID', (0,0), (-1,-1), 1, colors.black),
    ('BACKGROUND', (0,0), (-1,0), colors.lightblue),
    ]))
    return tabelle 
