// static/js/common.js


// =====================
// Hintergrundfarbe setzen
// =====================
function setBackgroundColor(kundennummer) {

    // Defaultfarbe, wenn kein Wert gesetzt ist
    const defaultColor = "rgb(173,216,230)";

    let color;
    if (kundennummer !== undefined && kundennummer !== null){
        const letzteZiffer = kundennummer % 10;
        const hue = (letzteZiffer * 36) % 360; // 10 mögliche Werte über Farbrad
        color = `hsla(${hue}, 40%, 65%, 0.8)`;
    } else {
        color = defaultColor
    }

    
    const kundenbereich = document.querySelector("#erfassung-header, #erfassung_bearbeiten-header, #rechnungen-header, #rechnung_bearbeiten-header");
    const upperMain = document.getElementById("upper-main");

    if (kundenbereich) kundenbereich.style.backgroundColor = color;
    // if (upperMain) upperMain.style.backgroundColor = color;
}
