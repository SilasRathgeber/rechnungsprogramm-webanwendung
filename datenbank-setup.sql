CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE IF NOT EXISTS "kunden" (
    id INTEGER PRIMARY KEY,
    name TEXT,
    strasse TEXT,
    hausnummer TEXT,
    plz TEXT,
    ort TEXT,
    aktueller_stundensatz REAL
, email TEXT);

CREATE TABLE rechnungen (
    id INTEGER PRIMARY KEY,
    kunde_id INTEGER NOT NULL,
    re_datum TEXT,
    abrechnungsart TEXT CHECK(abrechnungsart IN ('projekt', 'zeit')) NOT NULL,
    projekt TEXT,
    honorar REAL,
    bezahlt INTEGER NOT NULL DEFAULT 0, 
    verschickt INT DEFAULT 0, 
    ausgangsdatum DATE DEFAULT NULL, 
    erstellt INT DEFAULT 0,
    FOREIGN KEY (kunde_id) REFERENCES kunden(id),
    CHECK (
        (abrechnungsart = 'projekt' AND honorar IS NOT NULL AND projekt IS NOT NULL) OR
        (abrechnungsart = 'zeit' AND honorar IS NULL AND projekt IS NULL)
    )
);
CREATE TABLE zeiterfassungen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kunde_id INTEGER NOT NULL,
    rechnung_id INTEGER,
    von TEXT NOT NULL,
    bis TEXT NOT NULL, 
    stundensatz REAL DEFAULT 0.0,
    FOREIGN KEY (kunde_id) REFERENCES kunden(id),
    FOREIGN KEY (rechnung_id) REFERENCES rechnungen(id) ON DELETE CASCADE
);

CREATE TABLE zeiteintraege (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zeiterfassung_id INTEGER NOT NULL,
    datum TEXT NOT NULL,
    startzeit TEXT NOT NULL,
    endzeit TEXT NOT NULL,
    beschreibung TEXT,
    stunden REAL,
    stundensatz REAL,
    gesamt REAL,
    FOREIGN KEY (zeiterfassung_id) REFERENCES zeiterfassungen(id) ON DELETE CASCADE
);
