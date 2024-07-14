from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
import threading
from .cleanup import delete_old_files

db = SQLAlchemy()
DB_NAME = "User_database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ooga bonga kangaroo'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 31536000
    db.init_app(app)
    
   
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, File
    
    with app.app_context():
        db.create_all()
        
        files = File.query.all()
        for file in files:
            file.download_ready = 0
        db.session.commit()

    login_manager = LoginManager()
    login_manager.login_view = "views.how_to_use"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    def start_cleanup_thread():
        threading.Thread(target=delete_old_files).start()

    
    start_cleanup_thread()

    return app


def create_database(app):
    if not os.path.exists("website/" + DB_NAME):
        db.create_all(app = app)
        print("database created! ")


