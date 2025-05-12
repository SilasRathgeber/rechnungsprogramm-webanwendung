from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from rechnungsprogramm.config import LOGO_PATH, BERLINSANS_PATH
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path

# PDF-Datei erzeugen
def built_page():
    c = canvas.Canvas("rechnung_template.pdf", pagesize=A4)
    width, height = A4

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

    # PDF speichern
    c.save()

if __name__ == "__main__":
    built_page()