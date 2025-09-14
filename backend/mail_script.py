import smtplib
from email.message import EmailMessage
import mimetypes

def send_mail(dateipfad, message, empfaenger, betreff):

    # Nachricht erstellen
    msg = EmailMessage()
    msg['Subject'] = betreff
    msg['From'] = 'it@silas-rathgeber.de'    # dein Exchange-Mail
    msg['To'] = empfaenger
    msg.set_content(message)

    # Verbindung zu Exchange (Office 365) über SMTP
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_user = 'it@silas-rathgeber.de'
    smtp_pass = 'Urkunde1'

    # MIME-Typ bestimmen (z. B. application/pdf, image/png)
    mime_type, _ = mimetypes.guess_type(dateipfad)
    if mime_type is None:
        mime_type = "application/octet-stream"  # Fallback, wenn unbekannt
    maintype, subtype = mime_type.split("/", 1)

    with open(dateipfad, 'rb') as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=dateipfad.split("/")[-1]  # nur der Dateiname
        )

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # TLS aktivieren
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print("Mail erfolgreich verschickt!")
        return True
    except Exception as e:
        print("Fehler beim Verschicken:", e)
        return False

