from tabulate import tabulate
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import mm
from reportlab.lib import colors
from rechnungsprogramm.config import *
from rechnungsprogramm.get_data import get_kundennummer, get_excel_data
import pandas as pd
from reportlab.platypus import PageTemplate, Frame, Table
from reportlab.lib.pagesizes import A4
from rechnungsprogramm.build_canvas import zeichne_briefpapier

def get_kunden_daten():
    # Lies die Kundendaten aus der Kundentabelle anhand der Kundennummer
    KundenNummer = get_kundennummer(get_excel_data())
    print(f"\n Die Kundennummer lautet: '{KundenNummer}'.\n")

    # Lies die Kundenliste ein
    df = pd.read_excel(DATA_DIR/"Liste_Kunden.xlsx", engine="openpyxl")

    # Speichern der Zeile mit KndNr in einer Variablen
    Kunden_Zeile = df.loc[df['KndNr.'] == KundenNummer]
    kopf = list(Kunden_Zeile.columns)
    daten = Kunden_Zeile.values.tolist()
    return [kopf] + daten


def erstelle_rechnung(daten, pfad="rechnung.pdf"):
    doc = SimpleDocTemplate(pfad, pagesize=A4)

    frame = Frame(40, 40, 500, 750, id='Inhalt')
    template = PageTemplate(id='Briefpapier', frames=frame, onPage=zeichne_briefpapier)
    doc.addPageTemplates([template])

    tabelle = Table(daten)
    flowables = [tabelle]

    doc.build(flowables, onFirstPage=zeichne_briefpapier, onLaterPages=zeichne_briefpapier)


def generate_letter_head_table():

    print(tabulate(get_kunden_daten()))

    erstelle_rechnung(get_kunden_daten())

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

if __name__ == "__main__":
    generate_letter_head_table()