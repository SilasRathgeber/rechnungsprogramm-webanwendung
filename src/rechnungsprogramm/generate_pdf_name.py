from rechnungsprogramm.get_data import get_kundennummer_und_zeitraum

def generate_file_name(rechnungsnummer):

    kdr_zeitraum = get_kundennummer_und_zeitraum()
    kdr = kdr_zeitraum[0][0]
    anfangsdatum_lst = kdr_zeitraum[1][0]
    enddatum_lst = kdr_zeitraum[2][0]
    anfangsdatum = anfangsdatum_lst.strftime("%d.%m.%Y")
    enddatum = enddatum_lst.strftime("%d.%m.%Y")
    filename = f"Re{rechnungsnummer}_{anfangsdatum} - {enddatum}_KdNr_{kdr}.pdf"

    return filename

