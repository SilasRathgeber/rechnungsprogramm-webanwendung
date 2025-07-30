#!/bin/bash
echo "Starte mit Installation von SQLite3"
sudo apt update
sudo apt-get install sqlite3 -y

DATENBANKNAME=rechnungsprogramm_database.db

# Datenbank und Tabellen anlegen
sqlite3 $DATENBANKNAME < datenbank-setup.sql

# Beispiel: Inhalte ausgeben
echo "Inhalt der Tabelle kunden:"
sqlite3 $DATENBANKNAME "SELECT * FROM kunden;"