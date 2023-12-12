from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())

    # relationships
    events = db.relationship('Event', backref='user', passive_deletes=True)
    likes = db.relationship('Like', backref='user', passive_deletes=True)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eventName = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    category = db.Column(db.String, nullable=False)
    eventDate = db.Column(db.DateTime, nullable=False)
    eventPrice = db.Column(db.Integer, nullable=False)
    ticketsNo = db.Column(db.Integer, nullable=False)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())

    #relationships
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    likes = db.relationship('Like', backref='event', passive_deletes=True)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime(timezone=True), default=func.now())

    #relationships
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id', ondelete="CASCADE"), nullable=False)