# Rechnungsprogramm

# NEU: jetzt per pyproject.toml installieren! Befhel dazu:

pip install -e . #im Root-Verzeichnis des Projekts bzw. im Repository

# Aufruf des Programms noch über: 

PYTHONPATH=src python -m rechnungsprogramm.main data/zeiterfassung_januar.xlsx
..\..\OneDrive - Silas Rathgeber IT\Eigene Dokumente\Kleingewerbe - Silas Rathgeber IT-Dienstleistungen\Kunden\Claus Middelhuß\Zeiterfassung\2023

## Einrichtung der virtuellen Umgebung

1. Virtuelle Umgebung erstellen (falls noch nicht vorhanden):

python -m venv "Name deiner virtuellen Umgebung"

2. Virtuelle Umgebung aktivieren:

source venv_name/Scripts/activate

3. Abhängigkeiten installieren:

pip install -r requirements.txt

## Was noch zutun ist!!

26.05. Aktueller Status: Das Programm ist als Paket installierbar.

- die Briefkopftabelle wäre noch schön zum richtigen seitenrand nach rechts zu bringen. Vielleicht mit einer eigenen Tabelle

- Außerdem steht die OOP-risierung noch an.

- Schauen wie man die Dateneingabe einfacher gestallten kann (Mit Apps etc. (Möglicherweise Obsidian oder Anytype oder eigener Webseite))