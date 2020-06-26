from flask import Flask
from flask_sqlalchemy import SQLAlchemy, Pagination
from flask_migrate import Migrate
from .config import Config
from sqlalchemy import func

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def _update_db(obj):
    db.session.add(obj)
    db.session.commit()
    return obj


import routes, models