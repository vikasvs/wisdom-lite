from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
import os

# Load environment variables from .env file if it exists (not in testing)
if not os.environ.get('TESTING'):
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def _update_db(obj):
    db.session.add(obj)
    db.session.commit()
    return obj


import routes, models