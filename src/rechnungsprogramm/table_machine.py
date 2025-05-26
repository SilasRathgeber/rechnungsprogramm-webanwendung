from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib import colors
from datetime import datetime, date
from rechnungsprogramm.config import FRAMEWIDTH, FIRMEN_ADRESSE_ORT, FIRMEN_ADRESSE_STRASSE, FIRMEN_NAME
from rechnungsprogramm.generate_rechnungsnummer import generate_rechnungsnummer

def generate_invoice_head(kundendaten_gelistet: list, datensatz_mit_kdr_daten: list, rechnungsnummer) -> None:
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
        #spaceAfter=12,
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


def generate_invoice_content(viele_zeilen, kundendaten: list):

    STUNDENSATZ = kundendaten[6]

    styles = getSampleStyleSheet()
    ueberschriften_rechts = ParagraphStyle(
        name="ueberschriften_rechts",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName="CalibriB",
        fontSize=11,
        textColor=HexColor("#000000"),
        spaceAfter=12,
        leading=11,
        alignment=2
    )
    ueberschriften_links = ParagraphStyle(
        name="ueberschriften_links",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName="CalibriB",
        fontSize=11,
        textColor=HexColor("#000000"),
        spaceAfter=12,
        leading=11,
        alignment=0
    )
    data_content = ParagraphStyle(
        name="data_content",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName="Calibri",
        fontSize=11,
        textColor=HexColor("#000000"),
        spaceAfter=12,
        leading=11,
        alignment=2
    )
    style_beschreibung = ParagraphStyle(
        name="style_beschreibung",
        parent=styles["Normal"],           # <- sehr wichtig!
        fontName="Calibri",
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
    Zeilenanzahl = 0
    GESAMTBETRAG = 0
    for i, unterliste in enumerate(viele_zeilen):
            TAGESDATUM = None
            BESCHREIBUNG = None
            START = None
            STOP = None
            for j, element in enumerate(unterliste):
                if j==0:
                    TAGESDATUM = element.strftime("%d.%m.%Y")
                if j==2:
                    BESCHREIBUNG = element
                if j==3:
                    START = element
                if j==4:
                    STOP = element
            Zeilenanzahl += 1
            start_dt = datetime.combine(date.today(), START)
            stop_dt = datetime.combine(date.today(), STOP)
            dauer = stop_dt - start_dt
            dauer_stunden = round(dauer.total_seconds() / 3600, 2)
            stunden_mal_satz = round(STUNDENSATZ * dauer_stunden, 2)
            anzeige_start = START.strftime("%H:%M")
            anzeige_stop = STOP.strftime("%H:%M")
            GESAMTBETRAG += stunden_mal_satz
            zeile = [
                Paragraph(f"{BESCHREIBUNG}<br/><font color=#A6A6A6 size=8>{TAGESDATUM} {anzeige_start} - {anzeige_stop} Uhr</font>", style_beschreibung), 
                Paragraph(f"{dauer_stunden}".replace(".",","), data_content), 
                Paragraph(f"{STUNDENSATZ}", data_content),
                Paragraph(f"{stunden_mal_satz:.2f} €".replace(".",","), data_content)
            ]
            tabellen_struktur.append(zeile)

    letzte_zeile = [
         "", 
         "",
         Paragraph(f"Gesamtbetrag:", data_content),
         Paragraph(f"{GESAMTBETRAG:.2f} €".replace(".",","), data_content)
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
    ('LINEBELOW', (0,0), (-1,Zeilenanzahl), 0.5, colors.black),
    ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ('LINEBELOW', (2,Zeilenanzahl+1), (3,Zeilenanzahl+1), 0.5, colors.black),
    ('LINEBELOW', (2,Zeilenanzahl+2), (3,Zeilenanzahl+2), 0.5, colors.black),
    ]))
    return tabelle 
