// static/js/zeiterfassung_bearbeiten.js

const table = document.getElementById('zeiteintraege-table');
const editButton = document.getElementById('editButton');
const selectedIdInput = document.getElementById('selectedIdInput');
let selectedRow = null;

const selectedIdInputs = [
    document.getElementById('selectedIdInput'),
    document.getElementById('selectedIdInputLoesche'),
    // weitere falls vorhanden
];

table.querySelectorAll('#zeiteintraege-table tbody tr').forEach(row => {
    row.addEventListener('click', () => {
        if (selectedRow) selectedRow.classList.remove('selected');
        row.classList.add('selected');
        selectedRow = row;

        let zellen = row.querySelectorAll('td');
        let idAusZelle = zellen[0].textContent.trim(); // oder andere Spalte
        
        console.log("ID aus Zelle:", idAusZelle);

        selectedIdInputs.forEach(input => {
        if(input) input.value = idAusZelle;
        });

        editButton.disabled = false;
        // und andere Buttons ggf. auch aktivieren
    });
});

['wegDamit'].forEach(formId => {
    const form = document.getElementById(formId);
    if (form) {
        form.addEventListener('submit', function(e) {
            // Hidden input im gleichen Formular suchen:
            const hiddenInput = form.querySelector('input[type="hidden"]');
            if (!hiddenInput || !hiddenInput.value) {
                e.preventDefault();
                alert('Bitte zuerst eine Zeile auswählen!');
            }
        });
    }
});

document.querySelectorAll("#zeiteintraege-table tr").forEach(row => {
    row.addEventListener("dblclick", function() {
        editRow(this);
    });
});

let activeRow = null; // aktuell editierte Zeile

function editRow(row) {

    if(activeRow && activeRow !== row) {
        // Inputs in normale Zellen zurückwandeln, falls keine Änderung
        Array.from(activeRow.cells).forEach((cell, cellIndex) => {
            const input = cell.querySelector("input");
            if(input) {
                if(input.value === input.defaultValue) {
                    // --- DATUM (index 1) ---
                    if (cellIndex === 1) {
                        // YYYY-MM-DD → DD.MM.YYYY
                        if (input.value) {
                            const [yyyy, mm, dd] = input.value.split("-");
                            cell.innerText = `${dd}.${mm}.${yyyy}`;
                        } else {
                            cell.innerText = "";
                        }
                    }

                    // --- START / END ZEIT (index 2,3) ---
                    else if (cellIndex === 2 || cellIndex === 3) {
                        // HH:MM bleibt HH:MM
                        cell.innerText = input.value;
                    }

                    else {
                    cell.innerText = input.value;
                    }
                }
            }
        });
    }

    activeRow = row; // neue Zeile als aktiv setzen

    Array.from(row.cells).forEach((cell, index) => {
        // Nur bestimmte Spalten editierbar machen
        if ([1, 2, 3, 4].includes(index)) { // z.B. Datum, Start, End, Beschreibung, Stunden
            const current = cell.innerText;
            const input = document.createElement("input");
            if (index === 4) {
                input.type = "text";
                input.value = current;
                input.style.width = "100%";
                input.style.boxSizing = "border-box";
            }else if (index === 1){
                input.type = "date"
                const parts = current.split("."); // ["01","12","2025"]
                if(parts.length === 3){
                    input.value = `${parts[2]}-${parts[1]}-${parts[0]}`; // 2025-12-01
                }
            }
            else {
                input.type = "time"
                
                // Alles außer Zahlen und ":" entfernen
                let match = current.match(/(\d{1,2}):(\d{1,2})/);
                if (match) {
                    let hh = match[1].padStart(2,"0");
                    let mm = match[2].padStart(2,"0");
                    input.value = `${hh}:${mm}`;
                } else {
                    input.value = "00:00"; // Fallback
                }
                
            }
            
            input.defaultValue = input.value; // Wert merken zum Vergleich

            cell.innerText = "";
            cell.appendChild(input);

            input.addEventListener("blur", () => saveRow(row));
        }
    });
}

function saveRow(row) {
    const data = [];
    Array.from(row.cells).forEach((cell, index) => {
        // Falls Input existiert, nimm den Wert, sonst den Text
        const input = cell.querySelector("input");
        const value = input ? input.value : cell.innerText;
        data.push(value);
    });

    console.log("Sende row_data:", data);  // Debug

    fetch("/update_row", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({row_data: data})
    }).then(res => {
        if(res.ok) console.log("Row updated");
    });
}
// =====================
// Initialisierung
// =====================
document.addEventListener('DOMContentLoaded', () => {
    const header = document.getElementById("erfassung_bearbeiten-header");
    let kundennummer = 1000; // Fallback
    if (header && header.dataset.kundennummer) {
        kundennummer = parseInt(header.dataset.kundennummer, 10);
    }

    setBackgroundColor(kundennummer);
    // initTabs();
    // initTableSelection();
    // initFormValidation();
});

// document.getElementById("write_invoice_button").addEventListener("click", function (event) {
//     event.preventDefault(); // Verhindert sofortiges Ausführen

//     Swal.fire({
//         title: 'Passt alles?',
//         text: "Rechnung jetzt schreiben!",
//         // icon: 'warning',
//         showCancelButton: true,
//         confirmButtonColor: '#d33',
//         cancelButtonColor: '#3085d6',
//         confirmButtonText: 'Ja',
//         cancelButtonText: 'Abbrechen'
//     }).then((result) => {
//         if (result.isConfirmed) {
//             // Hier kannst du die Aktion ausführen
//             // z. B. Formular absenden oder Redirect
//             document.getElementById("write_invoice").submit();
//             // Beispiel: Redirect
//             // window.location.href = "/delete/123";
//         }
//     });
// });