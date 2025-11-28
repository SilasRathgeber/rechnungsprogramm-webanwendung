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

const mail_senden_button = document.getElementById("mail-senden-button");
mail_senden_button.style.cursor = "pointer"; 
mail_senden_button.addEventListener("click", (e) => {
    e.stopPropagation(); // WICHTIG: Verhindert, dass der Klick zum Document bubbelt
    document.getElementById("email-popup").style.display = "inline-block";
});

const minitabelle_link_oben = document.getElementById("minitabelle-links-oben");
minitabelle_link_oben.style.cursor = "pointer"; 
minitabelle_link_oben.addEventListener("click", (e) => {
    e.stopPropagation(); // WICHTIG: Verhindert, dass der Klick zum Document bubbelt
    document.getElementById("rechnungs-nr-popup").style.display = "inline-block";
});

const erstellt_tabelle = document.getElementById("minitabelle-erstellt");
erstellt_tabelle.style.cursor = "pointer";
erstellt_tabelle.addEventListener("click", (e) => {
    e.stopPropagation(); // WICHTIG: Verhindert, dass der Klick zum Document bubbelt
    document.getElementById("speicherort-popup").style.display = "inline-block";
});

const verschickt_tabelle = document.getElementById("verschickt-tabelle");
verschickt_tabelle.style.cursor = "pointer";
verschickt_tabelle.addEventListener("click", (e) => {
    e.stopPropagation(); // WICHTIG: Verhindert, dass der Klick zum Document bubbelt
    document.getElementById("ausgangsdatum-popup").style.display = "inline-block";
});

const minitabelle_rechts_oben = document.getElementById("minitabelle-rechts-oben");
minitabelle_rechts_oben.style.cursor = "pointer";
minitabelle_rechts_oben.addEventListener("click", (e) => {
    e.stopPropagation(); // WICHTIG: Verhindert, dass der Klick zum Document bubbelt
    document.getElementById("zeitraum-popup").style.display = "inline-block";
});



function openPopup(id){
    document.getElementById(id).style.display = "inline-block";
}
function closePopup(id) {
  document.getElementById(id).style.display = "none";
}


function closePopupOnOutsideClick(event) {
    const popups = document.querySelectorAll('.popup');
    let clickedInsidePopup = false;

    // Überprüfe, ob der Klick innerhalb eines Popups war
    popups.forEach(popup => {
        if (popup.contains(event.target)) {
            clickedInsidePopup = true;
        }
    });

    // Wenn außerhalb geklickt wurde, schließe alle Popups
    if (!clickedInsidePopup) {
        popups.forEach(popup => {
            popup.style.display = 'none';
        });
    }
}




// =====================
// Initialisierung
// =====================
document.addEventListener('DOMContentLoaded', () => {
    const header = document.getElementById(HEADER_ID);
    let kundennummer = header?.dataset.kundennummer ? parseInt(header.dataset.kundennummer, 10) : undefined;

    setBackgroundColor(kundennummer);

        
    // Event-Listener für Popups NACH der Initialisierung hinzufügen
    document.addEventListener('click', closePopupOnOutsideClick);
});
