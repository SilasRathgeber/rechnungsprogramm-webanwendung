# Rechnungsprogramm – Webanwendung

A web-based invoice management application built with Python and Flask. The app allows freelancers and small businesses to manage customers, track working hours, and generate professional PDF invoices — all from a browser interface.

---

## Features

- **Customer management** – Store and manage customer data including preferred salutation
- **Time tracking** – Record working hours per customer and billing period
- **Invoice generation** – Automatically generate PDF invoices from time tracking data
- **Invoice workflow** – Track invoice status: created → sent → paid
- **Email support** – Send invoices via email with customizable message templates
- **File management** – Invoices are stored locally with configurable save paths
- **Deployment-ready** – Runs as a systemd service behind Nginx on a Raspberry Pi

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| PDF Generation | ReportLab |
| Web Server | Nginx |
| Process Manager | systemd |
| Packaging | pyproject.toml |

---

## Installation

### Prerequisites

- Python 3.x
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/SilasRathgeber/rechnungsprogramm-webanwendung.git
cd rechnungsprogramm-webanwendung

# Install the package
pip install -e .
```

---

## Development

Stop the production service and start the Flask development server:

```bash
sudo systemctl stop rechnungsprogramm-webanwendung-flask.service

cd ~/rechnungsprogramm-webanwendung
source venv/bin/activate

export FLASK_APP=wsgi.py
export FLASK_ENV=development

flask run --host=0.0.0.0 --port=5000 --debug
```

When done, restart the production service:

```bash
sudo systemctl start rechnungsprogramm-webanwendung-flask
```

---

## Project Structure

```
rechnungsprogramm-webanwendung/
├── wsgi.py                  # Entry point
├── pyproject.toml           # Package configuration
├── config.py                # Configuration loader
├── build_invoice.py         # Invoice generation logic
├── build_template.py        # PDF template (letterhead, layout)
├── get_data.py              # Data retrieval helpers
├── table_machine.py         # Invoice table generation
├── generate_pdf_name.py     # PDF filename generation
├── generate_rechnungsnummer.py  # Invoice number logic
├── fonts.py                 # Font registration
└── templates/               # Flask HTML templates
```

---

## License

This project is for personal and educational use.
