from flask import Blueprint, render_template

from flask_login import login_required, current_user
views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/room-creation')
@login_required
def room_creation():
    return render_template("room_creation.html", user=current_user)

@views.route('/room-joining')
@login_required
def room_joining():
    return render_template("room_joining.html", user=current_user)

@views.route('/room-management')
@login_required
def room_management():
    return render_template("room_management.html", user=current_user)

