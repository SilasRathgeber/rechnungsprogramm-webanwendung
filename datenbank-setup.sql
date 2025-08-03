-- Kunden-Tabelle
CREATE TABLE IF NOT EXISTS kunden (
    id INTEGER PRIMARY KEY,
    name TEXT,
    strasse TEXT,
    hausnummer TEXT,
    plz TEXT,
    ort TEXT,
    stundensatz REAL
);

-- Rechnungen-Tabelle
CREATE TABLE IF NOT EXISTS rechnungen (
    id INTEGER PRIMARY KEY,
    kunde_id INTEGER NOT NULL,
    re_datum TEXT NOT NULL,
    abrechnungsart TEXT CHECK(abrechnungsart IN ('projekt', 'zeit')) NOT NULL,
    projekt TEXT,
    honorar REAL,
    bezahlt INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (kunde_id) REFERENCES kunden(id),
    CHECK (
        (abrechnungsart = 'projekt' AND honorar IS NOT NULL AND projekt IS NOT NULL) OR
        (abrechnungsart = 'zeit' AND honorar IS NULL AND projekt IS NULL)
    )
);

-- Zeiterfassungen-Tabelle
CREATE TABLE IF NOT EXISTS zeiterfassungen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kunde_id INTEGER NOT NULL,
    rechnung_id INTEGER,
    von TEXT NOT NULL,
    bis TEXT NOT NULL,
    FOREIGN KEY (kunde_id) REFERENCES kunden(id),
    FOREIGN KEY (rechnung_id) REFERENCES rechnungen(id)
);

-- Zeiteinträge-Tabelle
CREATE TABLE IF NOT EXISTS zeiteintraege (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zeiterfassung_id INTEGER NOT NULL,
    datum TEXT NOT NULL,
    startzeit TEXT NOT NULL,
    endzeit TEXT NOT NULL,
    beschreibung TEXT,
    stunden REAL,
    gesamt REAL,
    FOREIGN KEY (zeiterfassung_id) REFERENCES zeiterfassungen(id)
);
