from reportlab.lib.colors import black
from reportlab.lib.units import mm
from rechnungsprogramm.config import *
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.styles import getSampleStyleSheet

# PDF-Datei erzeugen
def zeichne_briefpapier(c, doc):
    # Füllfarbe setzen
    c.setFillColor(black)
    # Rechteck zeichnen: (x, y, breite, höhe)
    # Achtung: Der Nullpunkt ist links unten!
    rechteck_höhe = 10
    c.rect(0 * mm, (297-rechteck_höhe) * mm, 210 * mm, rechteck_höhe * mm, fill=1)

    logo_höhe_u_breite = 26.1 #quadratisch
    logo_abstand_z_l_rand = 12.76
    c.drawImage(LOGO_PATH,  logo_abstand_z_l_rand * mm, (297-rechteck_höhe-logo_höhe_u_breite-0.5) * mm, width= logo_höhe_u_breite * mm, height= logo_höhe_u_breite * mm, mask=None, preserveAspectRatio=True, anchor='s')

    # Schriftart registrieren
    pdfmetrics.registerFont(TTFont("BerlinSans", BERLINSANS_PATH))

    # Logoschrift setzen
    # Nullpunkt ist links unten! (Grundlinie)
    c.setFont("BerlinSans", 10)
    c.drawString((logo_abstand_z_l_rand+logo_höhe_u_breite+1.52) * mm, (297-rechteck_höhe-logo_höhe_u_breite/2-3.43) * mm, "Silas Rathgeber")

    # Fußzeilentabelle:

    Zelle1 = f"{FIRMEN_NAME}<br/>Steuer-ID: {FIRMEN_STEUER_ID}<br/>Steuernummer: {FIRMEN_STEUER_NR}<br/>USt-ID: {FIRMEN_UST_ID}"
    Zelle2 = f"{FIRMEN_ADRESSE_STRASSE}<br/>{FIRMEN_ADRESSE_ORT}<br/>Mobil: {FIRMEN_TEL}<br/>E-Mail: {FIRMEN_MAIL}"
    Zelle3 = f"Bankverbindung:<br/>{FIRMEN_KREDITINSTITUT}<br/>IBAN: {FIRMEN_IBAN}<br/>BIC: {FIRMEN_BIC}"

    ## Vorher Paragraph
    styles = getSampleStyleSheet()
    my_p_style = ParagraphStyle("Footer_Tabelle", parent=styles["Normal"], fontName="Calibri", fontSize=9, leading=9, spaceAfter=0, textColor=colors.HexColor("#3B3838"))

    daten = [
        [Paragraph(Zelle1, my_p_style),
         Paragraph(Zelle2, my_p_style),
         Paragraph(Zelle3, my_p_style)]
    ]

    tabelle = Table(daten, colWidths=[150,180,150])

    tabelle.setStyle(TableStyle([
        ("VALIGN", (0,0), (-1,-1), "TOP"),  # vertikale Ausrichtung: oben
        ('BACKGROUND', (0, 0), (-1, 0), colors.white),         # Kopfzeile grau
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#3B3838')),    # Text in Kopfzeile weiß
        ('ALIGN', (1, 0), (11, -1), 'LEFT'),                # Alles zentrieren
        ('FONTNAME', (0, 0), (-1, -1), "Calibri"),      # Kopfzeile fett
        ('FONTSIZE', (0, 0), (-1, -1), 9),                   # Schriftgröße überall
    ]))

    x = doc.leftMargin
    y = 20 * mm

    w, h = tabelle.wrapOn(c, doc.width, doc.bottomMargin)
    tabelle.drawOn(c, x, y)

    # Falzmarken setzen
    c.saveState()  # optional, um Einstellungen lokal zu halten
    c.setStrokeColorRGB(0, 0, 0)  # schwarz
    c.setLineWidth(0.3)  # dünne Linie

    x_start = 15
    y_pos_1_falz = (297-105) * mm
    y_pos_2_falz = (297-210) * mm
    x_end_falz = x_start + 10

    c.line(x_start, y_pos_1_falz, x_end_falz, y_pos_1_falz)
    c.line(x_start, y_pos_2_falz, x_end_falz, y_pos_2_falz)

    # Lochmarke
    x_end_loch = x_start + 15
    y_pos_loch = (297-148.5) * mm
    c.line(x_start, y_pos_loch, x_end_loch, y_pos_loch)

    c.restoreState()



if __name__ == "__main__":
    zeichne_briefpapier()