from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # request contains all of the data that was sent in the form
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() # looking for an entry in the database -- filtering by email and returns first result
        if user:
            if check_password_hash(user.password, password): # make sure the password in the form matches the password in the db
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True) # remembers that the user is logged in -- stored in the flask session
                return redirect(url_for('views.home')) # redirects user to home page after logging in
            else:
                flash('Incorrect password', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required  # makes sure you cannot access this route if you aren't logged in
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        # request contains all of the data that was sent in the form
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first() # check if email already exists
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user) # add new user to db
            db.session.commit() # update the db
            login_user(new_user, remember=True) # remembers that the user is logged in -- stored in the flask session
            flash('Account created!', category='success')
            return redirect(url_for('views.home')) # redirects user to home page 

    return render_template("sign_up.html", user=current_user)