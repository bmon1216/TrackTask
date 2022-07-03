"""
Title:      routes.py
Desc:       routes for tracktask program
"""
import os
import secrets

from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, logout_user, current_user, login_required

from tracktask import app, db, bcrypt
from tracktask.forms import RegistrationForm, LoginForm, UpdateAccountForm, \
    TaskForm
from tracktask.models import User, Task

""" Sample Data
tasks = [
    {
        'task_name': 'Create SimpleList application',
        'text': 'Create a program to act as a task organizer as well as showcase the Flask web framework',
        'date_posted': 'JUN-23-2022',
        'status': False,
        'date_complete': None,
    },
    {
        'task_name': 'Python certificate program',
        'text': 'Complete the 8 month program to learn how to make web applications using Python',
        'date_posted': 'AUG-22-2021',
        'status': True,
        'date_complete': 'JUN-09-2021',
    },
    {
        'task_name': 'Create MagicLookup',
        'text': 'MTG card lookup and database storage. Will use the Django framework',
        'date_posted': 'JUN-19-2022',
        'status': False,
        'date_complete': None,
    },
    {
        'task_name': 'Create GitHub account',
        'text': 'create an account and move projects to a public repo',
        'date_posted': 'SEP-22-2021',
        'status': True,
        'date_complete': 'SEP-27-2021',
    },
]
"""


@app.route("/", methods=['GET', 'POST', 'PUT'])
@app.route("/index", methods=['GET', 'POST', 'PUT'])
def index():
    """Index/Home page"""
    page = request.args.get('page', 1, type=int, )
    tasks = Task.query \
        .order_by(Task.date_posted.desc()) \
        .paginate(page=page,
                  per_page=4)  # limits number of items per page
    return render_template('index.jinja2', tasks=tasks)


@app.route("/about", methods=['GET'])
def about():
    """About page"""
    return render_template('about.jinja2', title='About')


# - - - - - - - - - - - - - - Account Methods - - - - - - - - - - - - - - #


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

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
        return redirect(url_for('login'))
    return render_template('register.jinja2', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(user_email=form.user_email.data).first()

        if user and bcrypt.check_password_hash(user.password,
                                               form.password.data):
            login_user(user, remember=form.remember.data)

            next_page = request.args.get('next')

            return redirect(next_page) if next_page else redirect(
                url_for('index'))
        else:
            flash(f'Login failed. Please check email and password', 'danger')
    return render_template('login.jinja2', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _unused, file_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(app.root_path,
                                'static/profile_pics',
                                picture_filename, )

    # resize an uploaded picture using the Pillow module
    output_size = (125, 125)
    resized_image = Image.open(form_picture)
    resized_image.thumbnail(output_size)
    resized_image.save(picture_path)

    return picture_filename


@app.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.user_name.data = current_user.user_name
        form.user_email.data = current_user.user_email

    image_file = url_for('static',
                         filename=f'profile_pics/{current_user.user_image}', )
    return render_template('account.jinja2',
                           title='Account',
                           image_file=image_file,
                           form=form, )


@app.route("/user/<string:user_name>")
def user_tasks(user_name):
    page = request.args.get('page', 1, type=int, )
    user = User.query.filter_by(user_name=user_name).first_or_404()
    tasks = Task.query.filter_by(author=user) \
        .order_by(Task.date_posted.desc()) \
        .paginate(page=page, per_page=5)
    return render_template('user_tasks.jinja2',
                           tasks=tasks,
                           user=user, )


# - - - - - - - - - - - - - - Task Methods - - - - - - - - - - - - - - #

@app.route("/task/<int:task_id>")
def task(task_id):
    queried_task = Task.query.get_or_404(task_id)
    return render_template('task.jinja2',
                           task_name=queried_task.task_name,
                           task=queried_task, )


@app.route("/task/<int:task_id>/update", methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    queried_task = Task.query.get_or_404(task_id)

    # verify that the user requesting to update is the original author
    if queried_task.author != current_user:
        abort(403)
    form = TaskForm()

    if form.validate_on_submit():
        queried_task.task_name = form.task_name.data
        queried_task.text = form.text.data
        db.session.commit()
        flash('Task has been updated.', 'success')
        return redirect(url_for('task', task_id=queried_task.id))

    elif request.method == 'GET':
        form.task_name.data = queried_task.task_name
        form.text.data = queried_task.text

    return render_template('create_task.jinja2',
                           title='Update Task',
                           legend='Update Task',
                           form=form, )


@app.route("/task/<int:task_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    # verify that the user requesting to update is the original author
    if task.author != current_user:
        abort(403)

    db.session.delete(task)
    db.session.commit()
    flash('Task has been deleted!', 'success')
    return redirect(url_for('index'))


@app.route("/task/new", methods=['GET', 'POST'])
@login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(task_name=form.task_name.data,
                    text=form.text.data,
                    author=current_user, )
        db.session.add(task)
        db.session.commit()
        flash(f'Task has been added.', 'success')
        return redirect(url_for('index'))

    return render_template('create_task.jinja2',
                           title='New Task',
                           legend='New Task',
                           form=form, )
