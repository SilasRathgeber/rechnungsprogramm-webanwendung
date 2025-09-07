#!/bin/bash

sudo systemctl daemon-reexec       # systemd neu laden (sicherheitshalber)
sudo systemctl daemon-reload       # neue Service-Datei einlesen
#sudo systemctl enable rechnungsprogramm.service   # beim Boot starten
sudo systemctl start rechnungsprogramm.service    # jetzt starten

# Status Check:
# sudo systemctl status rechnungsprogramm.service
#
# Log Check:
# journalctl -u rechnungsprogramm.service -n 50 --no-pager
