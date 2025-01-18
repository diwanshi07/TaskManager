from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import logging

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)

    setup_jwt_config(app)

    with app.app_context():
        from .models import Task, User
        db.create_all() 


    logging.basicConfig(filename='logs/app.log', level=logging.INFO)

    from .routes import Api, api

    api.init_app(app)

    @app.route('/login')
    def landing_page():
        return render_template('login.html')

    @app.route('/signup')
    def signup_page():
        return render_template('signup.html') 

    @app.route('/tasks')
    def tasks_page():
        return render_template('tasks.html')

    return app

def setup_jwt_config(app):
    global SECRET_KEY, EXPIRATION_TIME
    SECRET_KEY = app.config.get('JWT_SECRET_KEY', '8d3d-d6314f46411c')
    EXPIRATION_TIME = app.config.get('JWT_EXPIRATION_TIME', 3)