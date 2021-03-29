from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json


views = Blueprint('views', __name__) 

# the function below will be run whenever we go to '/'
@views.route('/', methods=['GET', 'POST']) # methods includes the types of requests that this route can accept
@login_required  # makes sure you cannot access this route if you aren't logged in
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('The note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note) # add note to the db
            db.session.commit() # update the db
            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():  
    note = json.loads(request.data) # turns into a python dictionary 
    noteId = note['noteId']
    note = Note.query.get(noteId) # look for the note that has that id
    if note:
        if note.user_id == current_user.id: # if the user owns the note, they can delete the note
            db.session.delete(note)
            db.session.commit()

    return jsonify({})