from pathlib import Path


# Datenpfade
BASE_DIR = Path(__file__).resolve().parent

SRC_DIR = BASE_DIR.parent

ROOT_DIR = SRC_DIR.parent

DATA_DIR = ROOT_DIR / "data"

LOGO_PATH = DATA_DIR / "logo_trans.jpg"

FONT_DIR = ROOT_DIR / "fonts"

BERLINSANS_PATH = FONT_DIR / "BRLNSR.TTF"


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

# Was soll ausgeführt werden, wenn config.py direkt aufgerufen wird:
if __name__ == "__main__":
    print(BASE_DIR)
    print(SRC_DIR)
    print(ROOT_DIR)
    print(DATA_DIR)
    print("Logo-Datei:", LOGO_PATH)
    print(FONT_DIR)
    print("Logoschriftart:", BERLINSANS_PATH)