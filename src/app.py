from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found_error(error):
    print('here')
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    print('here2')
    return render_template('500.html'), 500


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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new-note', methods=['POST', 'GET'])
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
            return not_found_error(e)
    else:
        return render_template('create-note.html')


@app.route('/notes')
def show_notes():
    notes = Note.query.order_by(Note.updated_at.desc()).all()
    return render_template('notes.html', notes=notes)


@app.route('/notes/<int:id>')
def show_note_detail(id):
    note = Note.query.get(id)
    return render_template('note-detail.html', note=note)


@app.route('/notes/<int:id>/history')
def show_note_history(id):
    note_changes = NoteHistory.query.filter_by(note_id=id).all()
    return render_template('note-history.html', note_changes=note_changes)


@app.route('/notes/<int:id>/delete')
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
        return internal_error(e)


@app.route('/notes/<int:id>/update', methods=['POST', 'GET'])
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
            return not_found_error(e)
    else:
        return render_template('update-note.html', note=note)


if __name__ == "__main__":
    app.run(debug=False)
