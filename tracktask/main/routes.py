"""
Title:      routes.py
Desc:       contains route functions for running base application methods
"""
from flask import render_template, request, Blueprint

from tracktask.models import Task

main = Blueprint('main', __name__)


# - - - - - - - - - - - - - - Main Methods - - - - - - - - - - - - - - #

@main.route("/", methods=['GET', 'POST', 'PUT'])
@main.route("/index", methods=['GET', 'POST', 'PUT'])
def index():
    """Index/Home page"""
    page = request.args.get('page', 1, type=int, )
    tasks = Task.query \
        .order_by(Task.date_posted.desc()) \
        .paginate(page=page,
                  per_page=4)  # limits number of items per page
    return render_template('index.jinja2', tasks=tasks)


@main.route("/about", methods=['GET'])
def about():
    """About page"""
    return render_template('about.jinja2', title='About')
