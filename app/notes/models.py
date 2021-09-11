from slugify import slugify
from sqlalchemy import event
from datetime import datetime

from app.database import db


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=False)
    text = db.Column(db.String(300), nullable=False, unique=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, unique=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, unique=False)

    def __repr__(self):
        return '<Note %r>' % self.id


class NoteHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note_id = db.Column(db.Integer, nullable=False, unique=False)
    name = db.Column(db.String(100), nullable=False, unique=False)
    text = db.Column(db.String(300), nullable=False, unique=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, unique=False)

    def __repr__(self):
        return '<NoteHistory %r>' % self.id


def init_db():
    db.create_all()