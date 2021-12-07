from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User, Room, Chore
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import date
import re
import psycopg2 
import psycopg2.extras
auth = Blueprint('auth', __name__)


def has_numbers(inputString):
    return bool(re.search(r'\d', inputString))


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
        payment = request.form.get('link')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater then 1 character.', category='error')
        elif has_numbers(firstName):
            flash('First name must not contain numbers.', category='error')
        elif len(lastname) < 2:
            flash('Last name must be greater than 1 character.', category='error')
        elif has_numbers(lastname):
            flash('Last name must not contain numbers.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, firstName=firstName, lastname=lastname, paymentLink=payment,
                            password=generate_password_hash(
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
        payment = request.form.get('payment')

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
        elif payment and len(payment) < 7:
            flash('Link must be at least 7 characters.', category='error')
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
            if payment:
                current_user.paymentLink = payment
                flash('Payment link updated', category='success')
            db.session.commit()

    return render_template("manage_account.html", user=current_user)


@auth.route('/chats')
@login_required
def chats():
    return render_template("chats.html", user=current_user)


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
    # current_user.payment = False
    # db.session.commit()
    # if request.form.get('complete'):
    # current_user.payment = True
    # db.session.commit()
    return render_template("make_payment.html", user=current_user)


DB_HOST = "localhost"
DB_NAME = "choresboard"
DB_USER = "postgres"
DB_PASS = "admin"
        
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST) 
 
@auth.route('/calendar')
@login_required
def index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("SELECT * FROM events ORDER BY id")
    calendar = cur.fetchall()  
    return render_template('calendar.html', calendar = calendar, user=current_user)
  
@auth.route("/insert",methods=["POST","GET"])
@login_required
def insert():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        print(title)     
        print(start)  
        cur.execute("INSERT INTO events (title,start_event,end_event) VALUES (%s,%s,%s)",[title,start,end])
        conn.commit()       
        cur.close()
        msg = 'success' 
    return render_template('calendar.html', user=current_user)
  
@auth.route("/update",methods=["POST","GET"])
@login_required
def update():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        id = request.form['id']
        print(title)     
        print(start)  
        cur.execute("UPDATE events SET title = %s, start_event = %s, end_event = %s WHERE id = %s ", [title, start, end, id])
        conn.commit()       
        cur.close()
        msg = 'success' 
    return render_template('calendar.html', user=current_user)    
  
@auth.route("/ajax_delete",methods=["POST","GET"])
@login_required
def ajax_delete():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        getid = request.form['id']
        print(getid)
        cur.execute('DELETE FROM events WHERE id = {0}'.format(getid))
        conn.commit()       
        cur.close()
        msg = 'Record deleted successfully' 
    return render_template('calendar.html',  user=current_user) 
