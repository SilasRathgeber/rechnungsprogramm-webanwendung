from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rechnungsprogramm.config import *

def registriere_schriftarten():
    #pdfmetrics.registerFont(TTFont("Calibri", CALIBRI_PATH))
    #pdfmetrics.registerFont(TTFont("CalibriB", CALIBRI_PATH_BOLT))
    #pdfmetrics.registerFont(TTFont("BerlingSans", BERLINSANS_PATH_REGULAR))
    #pdfmetrics.registerFont(TTFont("BerlingSansB", BERLINSANS_PATH_BOLT))
    pdfmetrics.registerFont(TTFont("Carlito", CARLITO))
    pdfmetrics.registerFont(TTFont("CarlitoB", CARLITO_BOLT))
    pdfmetrics.registerFont(TTFont("BloggerSans", BLOGGER_SANS))
    pdfmetrics.registerFont(TTFont("AncizarSerifB", ANCIZAR_SERIF_B))