from pathlib import Path
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from datetime import date
from appdirs import user_data_dir
import json
import pandas as pd

# Datenpfade
BASE_DIR = Path(__file__).resolve().parent

SRC_DIR = BASE_DIR.parent

ROOT_DIR = SRC_DIR.parent

DATA_DIR = ROOT_DIR / "data"

LOGO_PATH = BASE_DIR / "assets" / "images.jpg"

FONT_DIR = BASE_DIR / "fonts"

BLOGGER_SANS = FONT_DIR / "BloggerSans.ttf"

CARLITO = FONT_DIR / "Carlito-Regular.ttf"

CARLITO_BOLT = FONT_DIR / "Carlito-Bold.ttf"

ANCIZAR_SERIF_B = FONT_DIR / "AncizarSerif-Bold.ttf"

KANIT_B_I = FONT_DIR / "Kanit-BoldItalic.ttf"


# Wo steht die Kundennummer in der Exceldatei "Liste_Kunden.xlsx"?
KDNRX = 2
KDNRY = 2

# Firmen-Daten-Variablen:

FIRMEN_NAME = "Silas Rathgeber"
FIRMEN_ADRESSE_STRASSE = "Bürgermeister-Martin-Donandt-Platz 22"
FIRMEN_ADRESSE_ORT = "27568 Bremerhaven"
FIRMEN_TEL = "0157 31663270"
FIRMEN_MAIL = "it@silas-rathgeber.de"
FIRMEN_STEUER_ID = "65 019 332 843"
FIRMEN_STEUER_NR = "75 380 00226"
FIRMEN_UST_ID = "DE334028878"
FIRMEN_IBAN = "DE64 7435 0000 0004 5925 99"
FIRMEN_BIC = "BYLADEM1LAH"
FIRMEN_KREDITINSTITUT = "Sparkasse Landshut"


# Seitenlayout - Seitenränder:
LEFTMARGIN = 25 * mm
RIGHTMARGIN = 20 * mm
TOPMARGIN = 43 * mm
BOTTOMMARGIN = 45 * mm
PAGEWIDTH = A4[0]
FRAMEWIDTH = PAGEWIDTH - LEFTMARGIN -RIGHTMARGIN

# Pfad zu Default Ablageort Invoice und Log-Dateien
APP_NAME = "rechnungsprogramm"
APP_AUTHOR = "Silas Rathgeber"  # z. B. Silas
APP_VERSION = "1.0"
CONFIG_DIR = Path(user_data_dir(APP_NAME, APP_AUTHOR, APP_VERSION))
CONFIG_FILE = CONFIG_DIR / "rechnungsprogramm_config.json"
print(f"Die config.json liegt hier:\n{CONFIG_FILE}")
KUNDENLISTE_DEFAULT = CONFIG_DIR / "Liste_Kunden.xlsx"
INVOICE_LOG = CONFIG_DIR / "re_nr_log.txt"

#aktuelles_jahr = str(date.today().year)

DEFAULT_CONFIG = {
    "kundenliste": str(KUNDENLISTE_DEFAULT),
    "invoice_log": str(INVOICE_LOG),
    "logo": str(LOGO_PATH)
}

# Falls nötig, Verzeichnis & Dateien erzeugen
def initialize_config():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # Configdatei erzeugen
    if not CONFIG_FILE.exists():
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)


def load_config():
    initialize_config()
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

CONFIG = load_config()
KUNDENLISTE = Path(CONFIG["kundenliste"])
print(f"Verwendete Kundenliste:\n{KUNDENLISTE}")
INVOICE_LOG = Path(CONFIG["invoice_log"])
LOGO_PATH = Path(CONFIG["logo"])
print(f"Verwendetes Logo:\n{LOGO_PATH}")


# Exceldatei erzeugen, falls in der config.json noch der Default-Pfad angegeben ist und falls sie noch nicht vorhanden ist (gleiches für die log-Datei)
if KUNDENLISTE == KUNDENLISTE_DEFAULT:
    if not KUNDENLISTE_DEFAULT.exists():
        df = pd.DataFrame(columns=["KndNr.", "Name", "Straße", "Hausnummer", "Postleitzahl", "Ort", "Vereinbarter Stundensatz"])
        df.loc[0] = ["1000", "Müller", "Hauptstraße", "12a", "12345", "Berlin", 50]
        df.to_excel(KUNDENLISTE_DEFAULT, index=False)

    if not INVOICE_LOG.exists():
        INVOICE_LOG.write_text(f"0000\n", encoding="utf-8")

# Was soll ausgeführt werden, wenn config.py direkt aufgerufen wird:
if __name__ == "__main__":
    print(BASE_DIR)
    print(SRC_DIR)
    print(ROOT_DIR)
    print(DATA_DIR)
    print("Logo-Datei:", LOGO_PATH)
    print(FONT_DIR)
    print("Logoschriftart:", KANIT_B_I)