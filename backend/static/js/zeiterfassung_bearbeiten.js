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
// Optional: Falls kein Eintrag ausgewählt ist, Button deaktivieren
// (z.B. beim Laden oder nach Formular-Submit)


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

document.getElementById("write_invoice_button").addEventListener("click", function (event) {
    event.preventDefault(); // Verhindert sofortiges Ausführen

    Swal.fire({
        title: 'Passt alles?',
        text: "Rechnung jetzt schreiben!",
        // icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Ja',
        cancelButtonText: 'Abbrechen'
    }).then((result) => {
        if (result.isConfirmed) {
            // Hier kannst du die Aktion ausführen
            // z. B. Formular absenden oder Redirect
            document.getElementById("write_invoice").submit();
            // Beispiel: Redirect
            // window.location.href = "/delete/123";
        }
    });
});