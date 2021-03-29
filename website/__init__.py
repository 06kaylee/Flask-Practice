from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'change later'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # telling flask where the database is located
    db.init_app(app)

    # import blueprints
    from .views import views
    from .auth import auth

    # registering the blueprints -- telling flask where the blueprints are 
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # import to make sure that the models.py runs before creating db
    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # tells flask where you need to go to login
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):  # telling flask what user to look for and how we're referencing them (by id).
        return User.query.get(int(id))  # By default, looks for primary key and check if its equal to the id passed in.

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')