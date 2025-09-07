// static/js/rechnungen.js

// =====================
// Tabellenzeile auswählen
// =====================
function initTableSelection() {
    const table = document.getElementById('rechnungen-table');
    if (!table) return;

    const editButton = document.getElementById('editButton');
    let selectedRow = null;

    const selectedIdInputs = {
        id: document.getElementById('selectedIdInput'),
        loesch: document.getElementById('selectedIdInputLoesche')
    };

    table.querySelectorAll('tbody tr').forEach(row => {
        row.addEventListener('click', () => {
            if (selectedRow) selectedRow.classList.remove('selected');
            row.classList.add('selected');
            selectedRow = row;

            const zellen = row.querySelectorAll('td');
            if (zellen.length > 0) {
                if (selectedIdInputs.id) selectedIdInputs.id.value = zellen[0].textContent.trim();
                if (selectedIdInputs.loesch) selectedIdInputs.loesch.value = zellen[0].textContent.trim();
            }

            if (editButton) editButton.disabled = false;
        });
    });
}

// =====================
// Initialisierung
// =====================
document.addEventListener('DOMContentLoaded', () => {
    const header = document.getElementById("rechnungen-header");
    let kundennummer = undefined; 
    if (header && header.dataset.kundennummer) {
        kundennummer = parseInt(header.dataset.kundennummer, 10);
    }

    setBackgroundColor(kundennummer);
    // initTabs();
    initTableSelection();
    // initFormValidation();
});