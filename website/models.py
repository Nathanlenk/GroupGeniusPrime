from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import date


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    data = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(500), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    payment = db.Column(db.Boolean, default=False)
    paymentLink = db.Column(db.String(250))
    paymentDate = db.Column(db.Date, default=func.now())

    notes = db.relationship('Note')

    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))  # connect with room/ many-to-one
    chores = db.relationship('Chore')  # list of chores / User


class Room(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    roomName = db.Column(db.String(100), unique=True)
    roomCapacity = db.Column(db.Integer)
    admin_id = db.Column(db.Integer)  # default set to room's creator
    invitation_code = db.Column(db.String(20), default="")
    budget = db.Column(db.Float, default=0)

    users = db.relationship('User')  # list of users
    chores = db.relationship('Chore')  # list of chores / Room


class Chore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choreName = db.Column(db.String(30))
    description = db.Column(db.String(200))
    status = db.Column(db.Boolean, default=False)
    # due_date = db.Column(db.DateTime) # not ready

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # connect with user/ many-to-one
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))  # connect with room/ many-to-one
