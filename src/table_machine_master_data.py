from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
import subprocess

# Erstelle eine leere PDF-Datei
pdf_datei = "tabelle.pdf"



daten = [
    ["Bezeichnung", "Stunden", "€/h", "Gesamt"],     # Kopfzeile
    ["Service & Betreuung", 30, 15, ],
    ["Update Betreuung", "25", "25"],
    ["Allgemeiner Support", "40", "25"],
    ["", "" ,"Gesamtbetrag:", "22,50 €"]
]


tabelle = Table(daten)

tabelle.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.white),         # Kopfzeile grau
    ('LINEBELOW', (0, 0), (-1, 0), 0.5, colors.black),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),    # Text in Kopfzeile weiß
    ('ALIGN', (1, 0), (11, -1), 'CENTER'),                # Alles zentrieren
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),      # Kopfzeile fett
    ('FONTSIZE', (0, 0), (-1, -1), 12),                   # Schriftgröße überall
    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),               # Abstand unten Kopfzeile
    #('BACKGROUND', (0, 1), (-1, -1), colors.beige),       # Hintergrund restliche Zellen
    #('GRID', (0, 1), (-1, -1), 1, colors.red),          # Schwarzes Gitter überall
]))

elemente = [tabelle]  # Liste der Inhalte

breite, höhe = tabelle.wrap(0, 0)
dokument = SimpleDocTemplate(pdf_datei, pagesize=(breite, höhe),
                        topMargin=0, bottomMargin=0,
                        leftMargin=0, rightMargin=0)

# Schreibe die Inhalte ins PDF
dokument.build(elemente)

# Pfad zur erzeugten PDF
pdf_datei = "tabelle.pdf"

# Pfad zu SumatraPDF
sumatra_path = r"C:\\Users\\silas\\AppData\\Local\\SumatraPDF\\SumatraPDF.exe"

# PDF mit Sumatra öffnen
subprocess.Popen([sumatra_path, pdf_datei])