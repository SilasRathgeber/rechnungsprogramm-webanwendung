CREATE TABLE kunden (
    id INTEGER PRIMARY KEY,
    name TEXT,
    strasse TEXT,
    hausnummer TEXT,
    plz TEXT,
    ort TEXT,
    stundensatz REAL
);
CREATE TABLE rechnungen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kunde_id INTEGER NOT NULL,
    re_datum TEXT NOT NULL,
    zeitraum TEXT,
    projekt TEXT,
    FOREIGN KEY (kunde_id) REFERENCES kunden(id)
);
CREATE TABLE zeiterfassungen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kunde_id INTEGER NOT NULL,
    rechnung_id INTEGER,
    typ TEXT NOT NULL,
    FOREIGN KEY (kunde_id) REFERENCES kunden(id),
    FOREIGN KEY (rechnung_id) REFERENCES rechnungen(id)
);
CREATE TABLE zeiteintraege (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zeiterfassung_id INTEGER NOT NULL,
    datum TEXT NOT NULL,
    startzeit TEXT NOT NULL,
    endzeit TEXT NOT NULL,
    beschreibung TEXT,
    FOREIGN KEY (zeiterfassung_id) REFERENCES zeiterfassungen(id)
);
