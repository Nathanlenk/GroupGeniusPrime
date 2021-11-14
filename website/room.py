from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Room, Chore
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import random
import string

room = Blueprint('room', __name__)



@room.route('/room', methods=['GET', 'POST'])
@login_required
def room_dashboard():
    current_room_id = current_user.room_id
    current_room = Room.query.filter_by(id=current_room_id).first()
    if request.method == 'POST':
        roomLeave = request.form.get('roomLeave')
        if roomLeave == "Yes":
            current_user.room_id = None
            db.session.commit()
            return render_template("room.html", user=current_user, room=current_room)
    return render_template("room.html",user=current_user, room=current_room)

@room.route('/room-creation', methods=['GET', 'POST'])
@login_required
def room_creation():
    numbers = string.digits
    texts = string.ascii_uppercase
    invitation_code=''
    for i in range(5):
        invitation_code += random.choice(numbers)
        invitation_code += random.choice(texts)
    if request.method == 'POST':
        roomName = request.form.get('roomName')
        roomCapacity = request.form.get('roomCapacity')

    room = Room.query.filter_by(roomName=roomName).first()
    if room:
        flash('Room name already exists. Please pick another one.', category='error')
    elif len(roomName) < 3:
        flash('Room name must be greater than 2 characters.', category='error')
    elif len(roomName) > 99:
        flash('Your room name is too long!', category='error')
    elif int(roomCapacity) < 2:
        flash('Room capacity must be greater than 1.', category='error')
    else:
        new_room = Room(roomName=roomName, roomCapacity=int(roomCapacity), admin_id=current_user.id, budget=0, invitation_code=invitation_code)
        db.session.add(new_room)
        db.session.commit()
        flash('Room created!', category='success')
        current_room = Room.query.filter_by(roomName=roomName).first()
        current_user.room_id = current_room.id
        db.session.commit()
        return render_template("room.html", user=current_user,room=current_room)

    return render_template("room_creation.html", user=current_user)

@room.route('/room-joining', methods=['GET', 'POST'])
@login_required
def room_joining():
    if request.method == 'POST':
        roomName = request.form.get('roomName')
        invitation_code = request.form.get('invitation_code')
    roomSearch = Room.query.filter_by(roomName=roomName).first()

    if roomSearch:
        if invitation_code == roomSearch.invitation_code:
            flash(f'Joined {roomSearch.roomName}', category='success')
            current_user.room_id = roomSearch.id
            db.session.commit()
            return redirect(url_for('room.room_dashboard'))
        else:
            flash('Please re-check your invitation code', category='error')
    else:
        flash('There is no room with that name', category='error')
        return render_template("room_joining.html", user=current_user)


    
    return render_template("room.html", user=current_user, room=roomSearch)

@room.route('/room-management', methods=['GET', 'POST'])
@login_required
def room_management():
    if request.method == 'POST':
        roomName = request.form.get('roomName')
        roomCapacity = request.form.get('roomCapacity')
        roomBudget = request.form.get('budget')
        invitation_code = request.form.get('invitation_code')
    room=Room.query.filter_by(roomName=roomName).first()
    current_room = Room.query.filter_by(id=current_user.room_id).first()

    if room:
        flash('Room name already exists', category='error')
    elif roomName and len(roomName) < 3:
        flash('Room name must be greater than 2 characters.', category='error')
    elif roomName and len(roomName) > 99:
        flash('Your room name is too long!', category='error')
    elif roomCapacity and int(roomCapacity) < 2:
        flash('Room capacity must be greater than 1.', category='error')
    elif roomBudget and int(roomBudget) < 0:
        flash('Room budget must be greater than 0.', category='error')
    elif invitation_code and len(invitation_code) < 2:
        flash('Invitation code is too short', category='error')
    else:
        if roomName:
            current_room.roomName = roomName
            flash('Room name updated', category='success')
        if roomCapacity:
            current_room.roomCapacity = roomCapacity
            flash('Room capacity updated', category='success')
        if roomBudget:
            current_room.roomBudget = roomBudget
            flash('Room budget updated', category='success')
        if invitation_code:
            current_room.invitation_code = invitation_code
            flash('Room invitation code updated', category='success')
        db.session.commit()
        #current_room = Room.query.filter_by(roomName=room.roomName).first()

    return render_template("room_management.html", user=current_user)

