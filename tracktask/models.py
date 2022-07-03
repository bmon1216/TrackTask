"""
Title:      models.py
Desc:       App models using SQL_Alchemy
"""
from datetime import datetime
from flask_login import UserMixin

from tracktask import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    """Queries a user from user_id"""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User class model"""
    id = db.Column(db.Integer, primary_key=True, )
    user_name = db.Column(db.String(20), unique=True, nullable=False, )
    user_email = db.Column(db.String(100), unique=True, nullable=False, )
    user_image = db.Column(db.String(20), nullable=False, default='default.jpg', )
    password = db.Column(db.String(60), nullable=False, )
    tasks = db.relationship('Task', backref='author', lazy=True)

    def __repr__(self):
        """Returns when print() is called on object"""
        return f"User('{self.user_name}', '{self.user_email}', '{self.user_image}',"


class Task(db.Model):
    """Task class model"""
    id = db.Column(db.Integer, primary_key=True, )
    task_name = db.Column(db.String(100), nullable=False, )
    text = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, )
    status = db.Column(db.Boolean, nullable=False, default=False)
    date_complete = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """Returns when print() is called on object"""
        return f"User('{self.task_name}', '{self.text}',"
