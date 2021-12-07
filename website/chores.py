from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User, Room, Chore
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import date
import json

chores = Blueprint('chores', __name__)

@chores.route('/chores-board', methods=['GET', 'POST'])
@login_required
def chores_dashboard():
    current_room_id = current_user.room_id
    current_room = Room.query.filter_by(id=current_room_id).first()
    return render_template("chores_board.html",user=current_user, room=current_room)


@chores.route('/chore-creation', methods=['GET', 'POST'])
@login_required
def chore_creation():
    current_room_id = current_user.room_id
    current_room = Room.query.filter_by(id=current_room_id).first()
    if request.method == 'POST':
        choreName = request.form.get('choreName')
        description = request.form.get('description')
        day = int(request.form.get('day'))
        month = int(request.form.get('month'))
        year = int(request.form.get('year'))
        dueDate = date(year, month, day)
        roommate = request.form.get('roommate')

        assignee = User.query.filter_by(firstName=roommate).first()

        if len(choreName) < 2:
            flash(' Chore name is too short.', category='error')
        elif len(choreName) > 20:
            flash(' Chore name is too long.', category='error')
        else:
            new_chore = Chore(choreName=choreName,assignee= assignee.firstName, description=description,due_date = dueDate, user_id = int(assignee.id), room_id = int(current_room_id))
            db.session.add(new_chore)
            flash('Chore created!', category='success')
            db.session.commit()
            return render_template("chores_board.html", user=current_user,room=current_room)

    return render_template("chore_creation.html",user=current_user, room=current_room)

@chores.route('/chores-management', methods=['GET', 'POST'])
@login_required
def chores_management():
    current_room_id = current_user.room_id
    current_room = Room.query.filter_by(id=current_room_id).first()
    if request.method == 'POST':
        choreName = request.form.get('choreName')
        temp = choreName.split(" - ")
        choreName = temp[0]
        assigneeName = temp[1]
        choreName_new = request.form.get('choreName_new')
        description_new = request.form.get('description')
        day_new = int(request.form.get('day'))
        month_new = int(request.form.get('month'))
        year_new = int(request.form.get('year'))
        dueDate_new = date(year_new, month_new, day_new)
        roommate_new = request.form.get('roommate')

        #new_assignee = User.query.filter_by(firstName=roommate_new).first()
        chore = Chore.query.filter_by(choreName=choreName,assignee=assigneeName).first()

        if len(choreName_new) < 2:
            flash(' Chore name is too short.', category='error')
        elif len(choreName_new) > 20:
            flash(' Chore name is too long.', category='error')
        else:
            if choreName_new:
                chore.choreName = choreName_new
            if description_new:
                chore.description = description_new
            if dueDate_new:
                chore.due_date = dueDate_new
            if roommate_new:
                chore.assignee = roommate_new
            db.session.commit()
            flash('Chore updated', category='success')

    return render_template("chores_management.html",user=current_user, room=current_room)


@chores.route('/delete-chore', methods=['POST'])
@login_required
def delete_chore():
    chore = json.loads(request.data)
    choreID = chore['choreID']
    chore = Chore.query.get(choreID)
    if chore:
        db.session.delete(chore)
        db.session.commit()
    return jsonify({})

@chores.route('/check-chore', methods=['POST'])
@login_required
def check_chore():
    chore = json.loads(request.data)
    choreID = chore['choreID']
    chore = Chore.query.get(choreID)
    if chore:
        chore.status = 1
        db.session.commit()
    return jsonify({})

@chores.route('/uncheck-chore', methods=['POST'])
@login_required
def uncheck_chore():
    chore = json.loads(request.data)
    choreID = chore['choreID']
    chore = Chore.query.get(choreID)
    if chore:
        chore.status = 0
        db.session.commit()
    return jsonify({})

