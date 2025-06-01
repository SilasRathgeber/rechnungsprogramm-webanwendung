from rechnungsprogramm.config import INVOICE_LOG

if not INVOICE_LOG.exists():
    INVOICE_LOG.write_text("0000\n", encoding="utf-8")


def generate_rechnungsnummer():
    with open(INVOICE_LOG, "r", encoding="utf-8") as f:
        zeilen = f.readlines()

    letzte_zeile = zeilen[-1]
    letzte_nummer = int(letzte_zeile)

    neue_nummer = letzte_nummer + 1


    # Formatieren mit führenden Nullen
    formatiert = f"{neue_nummer:04d}"


    with open(INVOICE_LOG, "a", encoding="utf-8") as f:
        f.write(f"{formatiert}\n")

    return(formatiert)