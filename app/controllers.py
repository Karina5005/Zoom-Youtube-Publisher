from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    abort,
    redirect,
    url_for,
    current_app,
)
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from app.database import db

from app.notes.models import Note, NoteHistory
from app.general.controllers import handle_404, handle_500


module = Blueprint('notes', __name__)


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


@module.route('/')
def index():
    return render_template('index.html')


@module.route('/new-note', methods=['POST', 'GET'])
def create_note():
    if request.method == 'POST':
        name = request.form['name']
        text = request.form['text']
        note = Note(name=name, text=text)
        try:
            db.session.add(note)
            db.session.commit()
            note_history = NoteHistory(name=note.name, text=note.text, note_id=note.id, updated_at=datetime.utcnow())
            db.session.add(note_history)
            db.session.commit()
            return redirect('/new-note')
        except Exception as e:
            print(e)
            return handle_404(e)
    else:
        return render_template('create-note.html')


@module.route('/notes')
def show_notes():
    notes = Note.query.order_by(Note.updated_at.desc()).all()
    return render_template('notes.html', notes=notes)


@module.route('/notes/<int:id>')
def show_note_detail(id):
    note = Note.query.get(id)
    return render_template('note-detail.html', note=note)


@module.route('/notes/<int:id>/history')
def show_note_history(id):
    note_changes = NoteHistory.query.filter_by(note_id=id).all()
    return render_template('note-history.html', note_changes=note_changes)


@module.route('/notes/<int:id>/delete')
def delete_note(id):
    note = Note.query.get(id)
    note_changes = NoteHistory.query.filter_by(note_id=id).all()
    try:
        db.session.delete(note)
        db.session.commit()
        for note_change in note_changes:
            db.session.delete(note_change)
            db.session.commit()
        return redirect('/notes')
    except Exception as e:
        print(e)
        return handle_500(e)


@module.route('/notes/<int:id>/update', methods=['POST', 'GET'])
def update_note(id):
    note = Note.query.get(id)
    if request.method == 'POST':
        note.name = request.form['name']
        note.text = request.form['text']
        note.updated_at = datetime.utcnow()
        note_history = NoteHistory(name=note.name, text=note.text, note_id=note.id, updated_at=datetime.utcnow())
        try:
            db.session.add(note_history)
            db.session.commit()
            return redirect('/notes')
        except Exception as e:
            return handle_404(e)
    else:
        return render_template('update-note.html', note=note)
