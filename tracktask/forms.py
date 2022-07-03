"""
Title:      forms.py
Desc:       holds all form methods for TrackTask application
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, \
    ValidationError

from tracktask.models import User


class RegistrationForm(FlaskForm):
    """Registration of user accounts"""
    # validators are constraints
    user_name = StringField('Username',
                            validators=[DataRequired(), Length(min=4, max=20)])
    user_email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    # A custom validation to check for unique user_name
    def validate_user_name(self, user_name):
        user = User.query.filter_by(user_name=user_name.data).first()
        if user is not None:
            raise ValidationError('Username already exists.')

    # A custom validation to check for unique email
    def validate_user_email(self, user_email):
        email = User.query.filter_by(user_email=user_email.data).first()
        if email is not None:
            raise ValidationError('Email already exists.')


class LoginForm(FlaskForm):
    """Login of user accounts"""
    user_email = StringField('Email', validators=[DataRequired(), Email(), ])
    password = PasswordField('Password', validators=[DataRequired(),
                                                     Length(min=8, max=50), ])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    """Updates user account properties"""
    user_name = StringField('Username',
                            validators=[DataRequired(),
                                        Length(min=4, max=20)], )
    user_email = StringField('Email',
                             validators=[DataRequired(),
                                         Email()], )
    user_image = FileField('Update Profile Picture',
                           validators=[FileAllowed(['jpg',
                                                    'png',
                                                    'gif', ])], )
    submit = SubmitField('Update')

    # A custom validation to check for unique user_name
    def validate_user_name(self, user_name):
        if user_name.data != current_user.user_name:
            user = User.query.filter_by(user_name=user_name.data).first()
            if user is not None:
                raise ValidationError('Username already exists.')

    # A custom validation to check for unique email
    def validate_user_email(self, user_email):
        if user_email.data != current_user.user_email:
            email = User.query.filter_by(user_email=user_email.data).first()
            if email is not None:
                raise ValidationError('Email already exists.')


class TaskForm(FlaskForm):
    task_name = StringField('Task Name',
                            validators=[DataRequired()], )
    text = TextAreaField('Description',
                         validators=[DataRequired()], )
    submit = SubmitField('Submit Task')
