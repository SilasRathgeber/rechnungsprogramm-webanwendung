// static/js/rechnungen_bearbeiten.js

// =====================
// Selektoren & IDs
// =====================
const TABLE_ID = 'rechnungen-table';
const EDIT_BUTTON_ID = 'editButton';
const HEADER_ID = 'rechnung_bearbeiten-header';


// =====================
// Initialisierung
// =====================
document.addEventListener('DOMContentLoaded', () => {
    const header = document.getElementById(HEADER_ID);
    let kundennummer = header?.dataset.kundennummer ? parseInt(header.dataset.kundennummer, 10) : undefined;

    setBackgroundColor(kundennummer);
});
