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
[x] Auswählbarkeit der Rechnungen
[x] "Aktion"-Button der neue Seite für einzelne Rechnung	 öffnet
[x] Mit Zeiterfassung erstellen soll auch sofort der Rechnungs-Datensatz erstellt werden.
[x] neues Feld in rechnungen: Erstellt: ja/nein Dadurch entsteht eine Art Ladebalken von Erstellt - > verschickt -> bezahlt
[x] Dadurch wir der "Rechnung erstellen" Button obsolet
[x] Wenn Zeiterfassung gelöscht wird, muss auch Rechnungseintrag gelöscht werden (löschkaskade)
[x] Wenn man eine Zeiterfassung erstellt wird auch eine Rechnng erstellt aber nicht verknüpft!
[x] Wenn man eine Rechnung löscht wird die Seite ohne parameter neu aufgerufen schöner wäre wenn der kunde gleich wieder ausgewählt würde oder nur ein fetch asugeführt würde also ohne neuen Seiten aufruf
[x] die rechnungsnummer wird im rechnungsgenerator immer noch per log-datei erstellt. Das muss geändert werden. -> per sql via zeiterfassungs_id die zugehörige rechnungs_id ermitteln
[x] pfad nach OneDrive muss angepasst werden
[x] Speicherpfad in Datenbank hinterlegen? als Attribut? Dann könnte der Speicherpfad immer eingelesen werden und überprüft werden
[x] Wenn Rechnung erstellt wurde ist die Vorschau-funktion nicht mehr möglich sondern es wird immer die original-datei im iframe angezeigt
[x] Datumsangaben aus Datenbank umwandeln in europäisches Format
[x] Popup für E-Mail senden. Mit Möglichkeit, den Text anzupassen oder neues Attribut 'Anrede' in Kundendatenbank
[x] Funktion zum Einfügen eines Speicherpfads für alte Mails möglicherweise auch mit PopUP
[x] Speicherfunktion für Ausgangsdatum erstellen (rechnung bearbeiten seite)
[x] Bezahlt-funktion ertellen (rechnung bearbeiten seite)
[x] Bevorzugte Anrede als Attribut der Tabelle kunden hinzufügen, und beim Absenden der Email in den Standardtext alsl Variable einfügen
[x] Abrechnungszeitraum nachträglich ändern
[x] Seitenzahlen auf der Rechnung 
[x] Komma bei €/h auf der Rechnung
[ ] Wenn Rechnung verschickt wurde, darf das löschen nicht mehr möglich sein.
[ ] Löschen-Button auf der bearebeiten-Seite
[ ] Navigations-Button zur Zeiterfassung und von Zeiterfassung zurück zur Rechnung
[ ] KundenReminder zwischen Zeiterfassung und rechnungs-Menü
[ ] Doppelklick auf Datensatz für rechnungbearbeiten
[ ] Karteikarten für Zeiterfassung und Projektbezogene Abrechnung
[ ] Abrechnungstabelle zentrieren
[ ] Bei Popups wenn man irgendwo außerhalb des Popups klickt verschwindet das Popup
[ ] mehrere Zeiterfassungen einer Rechnung zuordnen
[ ] Entwicklungsversion von laufender Version trennen
[ ] Beim Hinzufügen von Zeiteintraegen den gültigkeitsbereich der Auswählbaren Tage auf den Abrechnungszeitraum
[ ] Rechnungsnummer erst dann vergeben, wenn auf "Rechnung jetzt erstellen" geklickt wird
[ ] Pfalzmarken hellgrauer machen
[ ] Kunden-Auswahl-Übergabe zwischen Rechnung und Zeiterfassung sowie zwischen Zeiterfassung und Zeiterfassung bearbeiten
[ ] In Zeiterfassungen filtern nach "Zeiterfassungen, die noch nicht abgerechnet wurden"