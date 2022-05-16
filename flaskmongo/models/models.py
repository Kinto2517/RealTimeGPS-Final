from flask_login import UserMixin
import pytz
from pytz import timezone
from datetime import datetime

from flaskmongo import login_manager, logindb

utc_now = datetime.utcnow()
utc = pytz.timezone('UTC')
aware_date = utc.localize(utc_now)
turkey = timezone('Europe/Istanbul')
now_turkey = aware_date.astimezone(turkey)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(logindb.Model, UserMixin):
    id = logindb.Column(logindb.Integer, primary_key=True)
    username = logindb.Column(logindb.String(20), unique=True, nullable=False)
    password = logindb.Column(logindb.String(20), nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"


class CarOwner (logindb.Model):
    id = logindb.Column(logindb.Integer, primary_key=True)
    car_id = logindb.Column(logindb.Integer, unique=True, nullable=True)
    user_id = logindb.Column(logindb.Integer, logindb.ForeignKey('user.id'), nullable=False)
    user_name = logindb.Column(logindb.String, logindb.ForeignKey('user.username'), nullable=False)


class LoginTime(logindb.Model):
    id = logindb.Column(logindb.Integer, primary_key=True)
    username = logindb.Column(logindb.String, logindb.ForeignKey('user.username'), nullable=False)
    date_login = logindb.Column(logindb.DateTime, nullable=False, default=now_turkey)
    user_id = logindb.Column(logindb.Integer, logindb.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"UserTime('{self.user_id}','{self.date_login}')"

class LogoutTime(logindb.Model):
    id = logindb.Column(logindb.Integer, primary_key=True)
    username = logindb.Column(logindb.String, logindb.ForeignKey('user.username'), nullable=False)
    user_id = logindb.Column(logindb.Integer, logindb.ForeignKey('user.id'), nullable=False)
    date_logout = logindb.Column(logindb.DateTime, nullable=False, default=now_turkey)

    def __repr__(self):
        return f"UserTime('{self.user_id}','{self.date_logout}')"