from pathlib import Path

def generate_rechnungsnummer():
    ordnetpfad_dieserdatei = Path(__file__).parent.parent.parent
    #print(ordnetpfad_dieserdatei)
    re_nr_log_pfad = ordnetpfad_dieserdatei / "data" / "re_nr_log.txt"
    with open(re_nr_log_pfad, "r", encoding="utf-8") as f:
        zeilen = f.readlines()

    letzte_zeile = zeilen[-1]
    letzte_nummer = int(letzte_zeile)

    neue_nummer = letzte_nummer + 1


    # Formatieren mit führenden Nullen
    formatiert = f"{neue_nummer:04d}"


    with open(re_nr_log_pfad, "a", encoding="utf-8") as f:
        f.write(f"{formatiert}\n")

    return(neue_nummer)