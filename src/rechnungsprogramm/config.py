from pathlib import Path


# Datenpfade
BASE_DIR = Path(__file__).resolve().parent

SRC_DIR = BASE_DIR.parent

ROOT_DIR = SRC_DIR.parent

DATA_DIR = ROOT_DIR / "data"

LOGO_PATH = DATA_DIR / "logo_trans.jpg"

FONT_DIR = ROOT_DIR / "fonts"

BERLINSANS_PATH = FONT_DIR / "BRLNSR.TTF"


# Wo steht die Kundennummer in der Exceldatei?
KDNRX = 2
KDNRY = 2

if __name__ == "__main__":
    print(BASE_DIR)
    print(SRC_DIR)
    print(ROOT_DIR)
    print(DATA_DIR)
    print("Logo-Datei:", LOGO_PATH)
    print(FONT_DIR)
    print("Logoschriftart:", BERLINSANS_PATH)