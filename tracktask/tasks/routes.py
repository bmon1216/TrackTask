"""
Title:      routes.py
Desc:       contains route functions that pertain to the tasks model
"""
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from tracktask import db
from tracktask.models import Task
from tracktask.tasks.forms import TaskForm

tasks = Blueprint('tasks', __name__)


# - - - - - - - - - - - - - - Task Methods - - - - - - - - - - - - - - #


@tasks.route("/task/<int:task_id>")
def task(task_id):
    queried_task = Task.query.get_or_404(task_id)
    return render_template('task.jinja2',
                           task_name=queried_task.task_name,
                           task=queried_task, )


@tasks.route("/task/<int:task_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('tasks.task', task_id=queried_task.id))

    elif request.method == 'GET':
        form.task_name.data = queried_task.task_name
        form.text.data = queried_task.text

    return render_template('create_task.jinja2',
                           title='Update Task',
                           legend='Update Task',
                           form=form, )


@tasks.route("/task/<int:task_id>/delete", methods=['GET', 'POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)

    # verify that the user requesting to update is the original author
    if task.author != current_user:
        abort(403)

    db.session.delete(task)
    db.session.commit()
    flash('Task has been deleted!', 'success')
    return redirect(url_for('main.index'))


@tasks.route("/task/new", methods=['GET', 'POST'])
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
        return redirect(url_for('main.index'))

    return render_template('create_task.jinja2',
                           title='New Task',
                           legend='New Task',
                           form=form, )
