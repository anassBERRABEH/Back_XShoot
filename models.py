from datetime import datetime
from config import db


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    folder = db.Column(db.String(120), unique=True, nullable=False)
    date = db.Column(db.Date, default=datetime.now)

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "folder": self.folder,
            "date": str(self.date)
        }
