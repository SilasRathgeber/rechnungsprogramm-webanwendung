// static/js/kunden.js

const loeschButton = document.getElementById('kunde_loesche_button');
    if (loeschButton) {
        loeschButton.addEventListener('click', function(e) {
            if (!confirm("Willst du das wirklich löschen?")) {
                e.preventDefault();
            }
        });
}