from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle

data = [['Empfänger:\nMax Mustermann\nMusterstraße 1\n12345 Musterstadt']]

table = Table(data, colWidths=200, rowHeights=80)

style = TableStyle([
    ('BOX', (0, 0), (-1, -1), 1, (0, 0, 0)),  # Rahmen um das Feld
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),      # Ausrichtung des Textes
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),      # Vertikale Ausrichtung (Text oben)
    ('LEFTPADDING', (0, 0), (-1, -1), 5),     # Abstand links vom Text
    ('TOPPADDING', (0, 0), (-1, -1), 5),      # Abstand oben
    ('RIGHTPADDING', (0, 0), (-1, -1), 5),    # Abstand rechts
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),   # Abstand unten
    ('TEXTCOLOR', (0, 0), (-1, -1), (0, 0, 0)),  # Textfarbe
])

table.setStyle(style)



# Datei anlegen
c = canvas.Canvas("rechnung.pdf", pagesize=A4)
width, height = A4  # Maße in Punkten

# Beispiel-Daten
kunde = "Max Mustermann"
rechnung_nr = "2025-001"
datum = "08.05.2025"
positionen = [
    ("Webdesign", 10, 50),
    ("Beratung", 5, 80)
]

c.build([table])

# Kopfbereich
c.setFont("Helvetica-Bold", 16)
c.drawString(20*mm, height - 30*mm, "RECHNUNG")
c.setFont("Helvetica", 12)
c.drawString(20*mm, height - 40*mm, f"Rechnungsnummer: {rechnung_nr}")
c.drawString(20*mm, height - 50*mm, f"Datum: {datum}")
c.drawString(20*mm, height - 60*mm, f"Kunde: {kunde}")

# Positionen
c.drawString(20*mm, height - 80*mm, "Leistung")
c.drawString(100*mm, height - 80*mm, "Stunden")
c.drawString(140*mm, height - 80*mm, "Betrag")

y = height - 90*mm
gesamt = 0
for leistung, stunden, preis in positionen:
    betrag = stunden * preis
    gesamt += betrag
    c.drawString(20*mm, y, leistung)
    c.drawRightString(120*mm, y, f"{stunden}")
    c.drawRightString(180*mm, y, f"{betrag:.2f} €")
    y -= 10*mm

# Gesamtsumme
c.setFont("Helvetica-Bold", 12)
c.drawRightString(180*mm, y - 10*mm, f"Gesamt: {gesamt:.2f} €")

c.save()

