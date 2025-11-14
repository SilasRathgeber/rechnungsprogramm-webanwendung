// static/js/rechnungen.js

// =====================
// Selektoren & IDs
// =====================
const TABLE_ID = 'rechnungen-table';
const EDIT_BUTTON_ID = 'editButton';
const HEADER_ID = 'rechnungen-header';

// =====================
// Hilfsfunktionen
// =====================

function createThreePointButton(reNr, kundeId, kundennummer){
    const button = document.createElement("button");
    button.textContent= "...";
    button.type= "button";
    button.classList.add("row-buttons")
    button.addEventListener("click", (e) => handleMenueClick(e, reNr, kundeId, kundennummer));
    return button;
}
function createDeleteButton(reNr, kundeId) {
    const button = document.createElement("button");
    button.textContent = "❌";
    button.type = "button";
    button.classList.add("row-buttons")
    button.addEventListener("click", (e) => handleDeleteClick(e, reNr, kundeId));
    return button;
}

function handleMenueClick(e, reNr, kundeId, kundennummer) {
    e.preventDefault();
    e.stopPropagation();

    submitMenueForm(reNr, kundeId, kundennummer);
}
function handleDeleteClick(e, reNr, kundeId) {
    e.preventDefault();
    e.stopPropagation();

    Swal.fire({
        title: `Rechnung ${reNr} löschen?`,
        text: `Achtung: Dadurch werden auch die zugehörige Zeiterfassung und alle Zeiteinträge gelöscht! Soll die Rechnung des Kunden ${kundeId} wirklich gelöscht werden?`,
        icon: "warning",
        showCancelButton: true,
        confirmButtonText: "Ja, löschen!",
        cancelButtonText: "Abbrechen"
    }).then((result) => {
        if (result.isConfirmed) {
            submitDeleteForm(reNr, kundeId);
        }
    });
}

function submitMenueForm(reNr, kundeId, kundennummer){
    const form = document.createElement("form");
    const header = document.getElementById(HEADER_ID);
    form.method = "POST";
    form.action = "/rechnungen";
    form.style.display = "none";

    const inputs = [
        { name: "reNr", value: reNr },
        { name: "aktion", value: "rechnung_detail" },
        { name: "kundenId", value: kundeId },
        { name: "selectedKundeReminder", value: kundennummer }
    ];

    

    inputs.forEach(({ name, value }) => {
        const input = document.createElement("input");
        input.type = "hidden";
        input.name = name;
        input.value = value;
        form.appendChild(input);
    });

    document.body.appendChild(form);
    form.submit();
}
function submitDeleteForm(reNr, kundeId) {
    const form = document.createElement("form");
    form.method = "POST";
    form.action = "/rechnungen";
    form.style.display = "none";

    const inputs = [
        { name: "reNr", value: reNr },
        { name: "aktion", value: "rechnung_loeschen" },
        { name: "kundenId", value: kundeId }
    ];

    inputs.forEach(({ name, value }) => {
        const input = document.createElement("input");
        input.type = "hidden";
        input.name = name;
        input.value = value;
        form.appendChild(input);
    });

    document.body.appendChild(form);
    form.submit();
}

// =====================
// Tabellenzeilen-Auswahl
// =====================
function initTableSelection(kundennummer) {
    const table = document.getElementById(TABLE_ID);
    if (!table) return;

    const editButton = document.getElementById(EDIT_BUTTON_ID);
    let selectedRow = null;

    table.querySelectorAll('tbody tr').forEach(row => {
        row.addEventListener('click', () => {
            // Alte Auswahl zurücksetzen
            if (selectedRow) {
                selectedRow.classList.remove('selected');
                const oldButtonsCell = selectedRow.querySelector('.zeilen-buttons-td');
                if (oldButtonsCell) oldButtonsCell.innerHTML = "";
            }

            // Neue Auswahl markieren
            row.classList.add('selected');
            const reNr = row.dataset.rechnungNr;
            const kundeId = row.dataset.kundeId;
            const buttonsCell = row.querySelector('.zeilen-buttons-td');

            // Löschen-Button und Dreipunkt-Button einfügen
            if (buttonsCell) {
                const deleteBtn = createDeleteButton(reNr, kundeId);
                buttonsCell.appendChild(deleteBtn);
                const menueBtn = createThreePointButton(reNr, kundeId, kundennummer);
                buttonsCell.appendChild(menueBtn);
            }

            selectedRow = row;
            if (editButton) editButton.disabled = false;
        });
    });
}

// =====================
// Feststellen, welcher Kunde ausgewählt ist
// =====================

function getSelectedSelect(){
    const kundeSelect = document.querySelector("#kundeFilterForm select[name='kunde_ausw_id']");

    if (kundeSelect) {
        // aktueller Wert (falls schon ausgewählt)
        console.log("Aktuell ausgewählt:", kundeSelect.value);

        // bei Änderung merken
        kundeSelect.addEventListener("change", (event) => {
            const selectedValue = event.target.value;
            console.log("Neu ausgewählt:", selectedValue);

            // z.B. in localStorage merken:
            localStorage.setItem("ausgewaehlterKunde", selectedValue);
        });
    }

    return(kundeSelect.value)

}

// =====================
// Initialisierung
// =====================
document.addEventListener('DOMContentLoaded', () => {
    const header = document.getElementById(HEADER_ID);
    let kundennummer = header?.dataset.kundennummer ? parseInt(header.dataset.kundennummer, 10) : undefined;


    selectedCustomer = getSelectedSelect();

    console.log("ausgewählter Kunde:", selectedCustomer);
    console.log("kundennummer", kundennummer);

    setBackgroundColor(kundennummer);
    initTableSelection(kundennummer);
});
