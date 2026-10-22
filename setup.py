import os, webbrowser, subprocess, sys
from threading import Timer

this_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(this_dir)

subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

from app import create_app
from app.extensions import db

app = create_app()
with app.app_context():
    db.create_all()

subprocess.Popen([sys.executable, "run.py"])
Timer(1.5, webbrowser.open, args=["http://127.0.0.1:5000"]).start()
