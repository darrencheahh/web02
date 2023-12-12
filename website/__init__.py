from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


db = SQLAlchemy()
DB_NAME = "database.db"

def create_web():
    web = Flask(__name__)
    web.config['SECRET_KEY'] = "web02"
    web.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(web)

    from .views import views
    from .auth import auth

    web.register_blueprint(views, url_prefix="/")
    web.register_blueprint(auth, url_prefix="/")

    from .models import User, Event, Like

    create_database(web)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(web)

    @login_manager.user_loader #get user information
    def load_user(id):
        return User.query.get(int(id))

    return web

#check if database is created
def create_database(web):
    db_path = path.join(web.root_path, 'static', DB_NAME)
    if not path.exists(db_path):
        with web.app_context():
            db.create_all()
        print("Created database")