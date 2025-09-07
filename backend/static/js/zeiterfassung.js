// static/js/zeiterfassung.js


// =====================
// Tabs initialisieren
// =====================
function initTabs() {
    const buttons = document.querySelectorAll(".tab-buttons button");
    const contents = document.querySelectorAll(".tab-content > .tab-content");

    contents.forEach(c => c.style.display = "none");
    const firstTab = document.getElementById("tab-1");
    if (firstTab) firstTab.style.display = "block";

    buttons.forEach(btn => {
        btn.addEventListener("click", () => {
            contents.forEach(c => c.style.display = "none");
            const target = document.getElementById(`tab-${btn.dataset.tab}`);
            if (target) target.style.display = "block";
        });
    });
}

// =====================
// Tabellenzeile auswählen
// =====================
function initTableSelection() {
    const table = document.getElementById('zeiterfassung-table');
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
// Formulare validieren
// =====================
function initFormValidation() {
    ['editForm', 'loescheZeitform'].forEach(formId => {
        const form = document.getElementById(formId);
        if (!form) return;

        form.addEventListener('submit', function(e) {
            const hiddenInput = form.querySelector('input[type="hidden"]');
            if (!hiddenInput || !hiddenInput.value) {
                e.preventDefault();
                alert('Bitte zuerst eine Zeile auswählen!');
            }
        });
    });

    const loeschButton = document.getElementById('loescheZeitform');
    if (loeschButton) {
        loeschButton.addEventListener('submit', function(e) {
            if (!confirm("Willst du das wirklich löschen?")) {
                e.preventDefault();
            }
        });
    }
}

// =====================
// Initialisierung
// =====================
document.addEventListener('DOMContentLoaded', () => {
    const header = document.getElementById("erfassung-header");
    let kundennummer = 1000; // Fallback
    if (header && header.dataset.kundennummer) {
        kundennummer = parseInt(header.dataset.kundennummer, 10);
    }

    setBackgroundColor(kundennummer);
    initTabs();
    initTableSelection();
    initFormValidation();
});
