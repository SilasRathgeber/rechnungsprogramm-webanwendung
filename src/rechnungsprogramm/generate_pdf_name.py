def generate_file_name(rechnungsnummer, report_head_infos):

    kdr_zeitraum = report_head_infos
    kdr = kdr_zeitraum[0]
    anfangsdatum_lst = kdr_zeitraum[1]
    enddatum_lst = kdr_zeitraum[2]
    anfangsdatum = anfangsdatum_lst.strftime("%d.%m.%y")
    enddatum = enddatum_lst.strftime("%d.%m.%y")
    filename = f"Re{rechnungsnummer}_{anfangsdatum} - {enddatum}_KdNr_{kdr}.pdf"

    return filename

