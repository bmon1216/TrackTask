"""
Title:      forms.py
Desc:       holds all task form methods
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class TaskForm(FlaskForm):
    task_name = StringField('Task Name',
                            validators=[DataRequired()], )
    text = TextAreaField('Description',
                         validators=[DataRequired()], )
    submit = SubmitField('Submit Task')

