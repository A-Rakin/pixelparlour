from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    caption = db.Column(db.String(200))
    filename = db.Column(db.String(100), nullable=False)
    thumbnail_filename = db.Column(db.String(100))
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    views = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Photo {self.title}>'