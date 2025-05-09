from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas

# Dokument mit SimpleDocTemplate erstellen
doc = SimpleDocTemplate("rechnung.pdf", pagesize=A4)

# Standard-Styles
styles = getSampleStyleSheet()

# Text-Abschnitt erstellen
text = Paragraph("Dies ist ein Beispiel für eine Rechnung.", styles['Title'])

# Tabelle erstellen
data = [["Artikel", "Menge", "Preis"],
        ["Widget", "2", "10 €"],
        ["Gadget", "5", "20 €"]]
table = Table(data)

# Canvas für individuelle Zeichnungen erstellen
c = canvas.Canvas("rechnung.pdf", pagesize=letter)

# Beispiel für Zeichnung: Eine Linie hinzufügen
c.line(100, 500, 500, 500)  # Zeichnet eine Linie auf die Seite

# Flowables zusammenstellen
flowables = [text, table]

# Dokument mit SimpleDocTemplate erstellen
doc.build(flowables)

# Weitere individuelle Zeichnungen können hier mit Canvas hinzugefügt werden
c.save()
