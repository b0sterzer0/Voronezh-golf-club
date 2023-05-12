from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


db = SQLAlchemy()


class Mail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String, unique=True, nullable=True)
    user = db.relationship('User', backref='mail')
    appeal = db.relationship('Appeal', backref='appeal')


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_number = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    mail_id = db.Column(db.Integer, db.ForeignKey('mail.id'), nullable=True)
    is_admin = db.Column(db.Boolean)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String)
    date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String, nullable=False)
    ticket_price = db.Column(db.Integer, nullable=False)


class Appeal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=True)
    mail_id = db.Column(db.Integer, db.ForeignKey('mail.id'))
    message = db.Column(db.Text)
    join_to_club = db.Column(db.Boolean, default=False, nullable=False)


class SiteData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    club_name = db.Column(db.String)
    email = db.Column(db.String)
    phone_number = db.Column(db.String)
    city = db.Column(db.String)
    address = db.Column(db.String)
    club_history = db.Column(db.Text)
    work_hours_weekdays = db.Column(db.String)
    work_hours_weekend = db.Column(db.String)
    url_video_on_main_page = db.Column(db.String)
