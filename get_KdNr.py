import pandas as pd
import sys

# Stecke den String, der als erstes Argument übergeben wurde in eine Variable
excel_datei = sys.argv[1]

# Lese mit der Pandas-Instanz die Datei ein, und speicher den DataFrame in einer Variable
df = pd.read_excel(excel_datei, engine="openpyxl")
# Nimm aus dem gespeicherten DataFrame nur eine bestimmte Zelle und speicher sie
KundenNummer = df.iloc[2, 2]

sys.stdout.write(str(KundenNummer))