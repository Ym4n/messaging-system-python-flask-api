from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager

db = SQLAlchemy()

import click
from flask.cli import with_appcontext

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()

def create_app(config_class=Config):
    # Flask init
    app = Flask(__name__)
    app.config.from_object(config_class)

    # DB init
    db.init_app(app)

    # login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from app.db_users import User

    @login_manager.user_loader
    def load_user(user_id):
        return db_users.User.query.get(int(user_id))

    from app.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.msg_api import msgapi_bp
    app.register_blueprint(msgapi_bp)

    from app.pages import pages_bp
    app.register_blueprint(pages_bp)
    
    app.cli.add_command(create_tables)

    return app


from app import db_users, db_msg
