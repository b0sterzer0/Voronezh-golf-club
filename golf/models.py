# from sqlalchemy import create_engine
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session
# from dotenv import load_dotenv, dotenv_values
# from werkzeug.security import generate_password_hash
#
#
# load_dotenv()
# DB_NAME = dotenv_values('.env')['DB_NAME']
# DB_PASSWORD = dotenv_values('.env')['DB_PASSWORD']
# HOST = dotenv_values('.env')['HOST']
# PORT = dotenv_values('.env')['PORT']
# USERNAME = dotenv_values('.env')['USERNAME']
#
# engine = create_engine(f"postgresql+psycopg2://{USERNAME}:{DB_PASSWORD}@{HOST}:{PORT}/{DB_NAME}", echo=True)
# db_session = Session(engine)
#
#
# class Base(DeclarativeBase):
#     pass
#
#
# class User(Base):
#     __tablename__ = 'User'
#
#     id: Mapped[int] = mapped_column(primary_key=True)
#     account_number: Mapped[str]
#     password: Mapped[str] = mapped_column(str(40))
#     is_admin: Mapped[bool]
#
#     def __repr__(self):
#         return f'User(id={self.id}), account_number={self.account_number}'

# Base.metadata.create_all(bind=engine)

# test_user = User(account_number='000000', password=generate_password_hash('12345'))
#
# session.add(test_user)
# session.commit()

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
