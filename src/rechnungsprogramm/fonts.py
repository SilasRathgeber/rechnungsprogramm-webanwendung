from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rechnungsprogramm.config import *

def registriere_schriftarten():
    pdfmetrics.registerFont(TTFont("Calibri", CALIBRI_PATH))
    pdfmetrics.registerFont(TTFont("BerlingSans", BERLINSANS_PATH))