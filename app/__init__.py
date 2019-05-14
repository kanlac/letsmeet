from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

bootstrap = Bootstrap()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:tbu33p6r9@localhost/letsmeet'
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = 'hard to guess string'
    db = SQLAlchemy(app)
    bootstrap = Bootstrap(app)
    
    return app

