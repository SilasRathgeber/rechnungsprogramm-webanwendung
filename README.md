# Rechnungsprogramm

# NEU: jetzt per pyproject.toml installieren! Befhel dazu:

pip install -e . #im Root-Verzeichnis des Projekts bzw. im Repository

# Weiterentwickeln? Dann das hier machen: 

sudo systemctl stop rechnungsprogramm-webanwendung-flask.service

cd ~/rechnungsprogramm-webanwendung

source venv/bin/activate

export FLASK_APP=wsgi.py
export FLASK_ENV=development

flask run --host=0.0.0.0 --port=5000 --debug

# Fertig mit Entwickeln? Dann das hier machen:

sudo systemctl start rechnungsprogramm-webanwendung-flask


## Einrichtung der virtuellen Umgebung

1. Virtuelle Umgebung erstellen (falls noch nicht vorhanden):

python -m venv "Name deiner virtuellen Umgebung"

2. Virtuelle Umgebung aktivieren:

source venv_name/Scripts/activate

3. Abhängigkeiten installieren:

pip install -r requirements.txt

## Was noch zutun ist!!

01.07.2025 Aktueller Status: Das Programm funktioniert

Verbesserungen:

- Mehr Ausgaben zu 1. Ist die Datei erfolgreich erstellt worden?
- In Config.json Pfad für Ablage anbieten ansonsten Ablage an Or und Stelle
- Funktion, die den  Ablageordnet mit der Rechnungsnummer-Log-Datei vergleicht
- Falls nicht vor dem Erstellen fragt, welche Nummer vergeben werden soll

26.05.2025 Aktueller Status: Das Programm ist als Paket installierbar.

- die Briefkopftabelle wäre noch schön zum richtigen seitenrand nach rechts zu bringen. Vielleicht mit einer eigenen Tabelle

- Außerdem steht die OOP-risierung noch an.

- Schauen wie man die Dateneingabe einfacher gestallten kann (Mit Apps etc. (Möglicherweise Obsidian oder Anytype oder eigener Webseite))

- Pfad Configuration möglich machen über eine config.json


## Projektstruktur

build_invoice.py
	erstelle_rechnungn()
build_template.py
	zeichne_briefpapier(c,doc)
	zeichne_betreff(c, doc)
	zeichne_anrede(c, doc)
	on_the_first_page(c, doc)
	on_later_pages(c, doc)
config.py
	initialize_config()
	load_config()
fonts.py
	registriere_schriftarten()
generate_pdf_name.py
	generate_file_name()
generate_rechnungsnummer.py
	generate_rechnungsnummer()
get_data.py
	get_excel_file_name()
	get_kundennummer_und_zeitraum()
	get_preiod_out_of_excel()
	get_time_data_out_of_excel()
	get_kunden_daten()
main.py
	main() 
table_machine.py
	generate_invoice_head()
	generate_invoice_content()


02.08.2025

Ideen Datenbankänderungen
- Anzahl Zeiteintraege bei Zeiterfassungstabelle anzeigen
- Monatsauswahl bei Zeiterfassungserstellungsformular
- Stundensatz auf Zeiterfassung/bearbeiten funktion/formular 

wo bin ich stehen geblieben am 23.08.25:
im template zeiterfassung_bearbeiten.html ein Form erstellen, mit dem man den Stundensatz anpassen kann

das machst du als nächstes:
- Auswählbarkeit der Rechnungen
- "Aktion"-Button der neue Seite für einzelne Seite öffnet