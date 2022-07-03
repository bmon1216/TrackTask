"""
Title:      __init__.py
Desc:       initializes components for TrackTask application
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from tracktask.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


def create_app(config_class=Config):
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from tracktask.users.routes import users
    from tracktask.tasks.routes import tasks
    from tracktask.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(tasks)
    app.register_blueprint(main)

    return app
