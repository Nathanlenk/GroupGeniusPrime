from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Room, Chore
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import date

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password or Email, please try again.', category='error')
        else:
            flash('Incorrect Password or Email, please try again.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastname = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater then 1 character.', category='error')
        elif len(lastname) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, firstName=firstName, lastname=lastname, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign-up.html", user=current_user)


@auth.route('/manage-account', methods=['GET', 'POST'])
@login_required
def manage_account():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastname = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif email and len(email) < 5:
            flash('Email must be greater than 3 characters.', category='error')
        elif firstName and len(firstName) < 2:
            flash('First name must be greater then 1 character.', category='error')
        elif lastname and len(lastname) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif password1 and len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            if email:
                current_user.email = email
                flash('Email updated', category='success')
            if firstName:
                current_user.firstName = firstName
                flash('First name updated', category='success')
            if lastname:
                current_user.lastname = lastname
                flash('Last name updated', category='success')
            if password1:
                current_user.password = generate_password_hash(password1, method='sha256')
                flash('Password updated', category='success')
            db.session.commit()

    return render_template("manage_account.html", user=current_user)


@auth.route('/chats')
@login_required
def chats():
    return render_template("chats.html", user=current_user)


@auth.route('/chores-board')
@login_required
def chores_board():
    return render_template("chore_board.html", user=current_user)


@auth.route('/make-payment', methods=['GET', 'POST'])
@login_required
def make_payment():
    if request.method == 'POST':
        if request.form.get('date'):
            newdate = request.form.get('date')
            year = int(newdate[:4])
            month = int(newdate[5:7])
            day = int(newdate[8:10])
            current_user.paymentDate = date(year, month, day)
            db.session.commit()
        if request.form.get('finish'):
            current_user.payment = True
            db.session.commit()
        if request.form.get('change'):
            if current_user.payment:
                current_user.payment = False
            else:
                current_user.payment = True
            db.session.commit()
       # if request.form.get('due'):
            #current_user.payment = False
            #db.session.commit()
        #if request.form.get('complete'):
            #current_user.payment = True
            #db.session.commit()
    return render_template("make_payment.html", user=current_user)
