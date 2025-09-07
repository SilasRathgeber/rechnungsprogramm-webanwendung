sudo systemctl stop rechnungsprogramm-webanwendung-flask.service
source /home/pi/rechnungsprogramm-webanwendung/venv/bin/activate
export FLASK_APP=wsgi.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5002 --debug
