from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.lib import colors

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        # Statt die Seite direkt zu rendern, speichern wir nur den Zustand
        self._saved_page_states.append(dict(self.__dict__))
        # Canvas wird nicht sofort gerendert!
        self._startPage()

    def save(self):
        total_pages = len(self._saved_page_states)
        for i, state in enumerate(self._saved_page_states, start=1):
            self.__dict__.update(state)
            self._pageNumber = i
            
            # Schriftfarbe setzen
            self.setFillColor(colors.HexColor("#3B3838"))  # dunkles Grau
            self.setFont("Carlito", 6)
            
            self.drawRightString(15*mm, 10*mm, f"{i} von {total_pages}")
            super().showPage()
        super().save()
