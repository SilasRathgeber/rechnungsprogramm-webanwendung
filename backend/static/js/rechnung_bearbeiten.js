// static/js/rechnungen_bearbeiten.js

// =====================
// Selektoren & IDs
// =====================
const TABLE_ID = 'rechnungen-table';
const EDIT_BUTTON_ID = 'editButton';
const HEADER_ID = 'rechnung_bearbeiten-header';


function emailTrigger(){
    const senden_button = getElementById('mail-senden-button')

    senden_button.addEventListener('click', (e) => handleSendClick(e))

}
    
function handleSendClick(){
    
}

const minitabelle_link_oben = document.getElementById("minitabelle-links-oben");
minitabelle_link_oben.style.cursor = "pointer"; 
minitabelle_link_oben.addEventListener("click", () => {
    document.getElementById("rechnungs-nr-popup").style.display = "inline-block";
});
const erstellt_tabelle = document.getElementById("minitabelle-erstellt");
erstellt_tabelle.style.cursor = "pointer";
erstellt_tabelle.addEventListener("click", () => {
    document.getElementById("speicherort-popup").style.display = "inline-block";
})
const verschickt_tabelle = document.getElementById("verschickt-tabelle");
verschickt_tabelle.style.cursor = "pointer";
verschickt_tabelle.addEventListener("click", () => {
    document.getElementById("ausgangsdatum-popup").style.display = "inline-block";
})

function openPopup(id){
    document.getElementById(id).style.display = "inline-block";
}
function closePopup(id) {
  document.getElementById(id).style.display = "none";
}



// =====================
// Initialisierung
// =====================
document.addEventListener('DOMContentLoaded', () => {
    const header = document.getElementById(HEADER_ID);
    let kundennummer = header?.dataset.kundennummer ? parseInt(header.dataset.kundennummer, 10) : undefined;

    setBackgroundColor(kundennummer);
});
