from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
import subprocess
import pandas as pd
import sys

# Hole den Dateinamen aus den Kommandozeilen-Argumenten
if len(sys.argv) != 2:
    print("Bitte eine Excel-Datei als Argument übergeben. (Endung .xlsx)")
    sys.exit()

# Stecke den String, der als erstes Argument übergeben wurde in eine Variable
excel_datei = sys.argv[1]

# Lies die Kundendaten aus der Kundentabelle anhand der Kundennummer
KundenNummer = subprocess.check_output(['python', 'get_KdNr.py', excel_datei], text=True)
KundenNummerInt = int(KundenNummer.strip())

# Lies eine andere Datei ein
df = pd.read_excel("Liste_Kunden.xlsx", engine="openpyxl")

# Speichern der Zeile mit KndNr in einer Variablen
Kunden_Zeile = df.loc[df['KndNr.'] == KundenNummerInt]

print(Kunden_Zeile.to_string())

'''
# Erstelle eine leere PDF-Datei
pdf_datei = "briefkopf_tabelle.pdf"



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

'''