"""
Title:      routes.py
Desc:       contains route functions that pertain to the users model
"""
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from tracktask import db, bcrypt
from tracktask.models import User, Task
from tracktask.users.forms import (RegistrationForm, LoginForm,
                                   UpdateAccountForm, )
from tracktask.users.utils import save_picture

users = Blueprint('users', __name__)


# - - - - - - - - - - - - - - Account Methods - - - - - - - - - - - - - - #


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')

        user = User(user_name=form.user_name.data,
                    user_email=form.user_email.data,
                    password=hashed_password, )

        db.session.add(user)
        db.session.commit()

        flash(f'Your account has been created!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.jinja2', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(user_email=form.user_email.data).first()

        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(
                url_for('main.index'))
        else:
            flash(f'Login failed. Please check email and password', 'danger')
    return render_template('login.jinja2', title='Login', form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@users.route("/account", methods=['GET', 'POST'])
@login_required  # needs to be after @app.route deco
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():

        if form.user_image.data:
            picture_file = save_picture(form.user_image.data)
            current_user.user_image = picture_file

        current_user.user_name = form.user_name.data
        current_user.user_email = form.user_email.data
        db.session.commit()
        flash('Account info updated.', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.user_name.data = current_user.user_name
        form.user_email.data = current_user.user_email

    image_file = url_for('static',
                         filename=f'profile_pics/{current_user.user_image}', )
    return render_template('account.jinja2',
                           title='Account',
                           image_file=image_file,
                           form=form, )


@users.route("/user/<string:user_name>")
def user_tasks(user_name):
    page = request.args.get('page', 1, type=int, )
    user = User.query.filter_by(user_name=user_name).first_or_404()
    tasks = Task.query.filter_by(author=user) \
        .order_by(Task.date_posted.desc()) \
        .paginate(page=page, per_page=5)
    return render_template('user_tasks.jinja2',
                           tasks=tasks,
                           user=user, )
