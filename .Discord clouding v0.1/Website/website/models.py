from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default = func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class File(db.Model , UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(100))
    progress = db.Column(db.String(100), default="uploading...")
    download_ready = db.Column(db.Integer, default=0)
    upload_ready = db.Column(db.Integer, default=0) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    file_path = db.Column(db.String(200)) #location stored by the user on the GUI (not implemented yet)
    date = db.Column(db.DateTime(timezone=True), default=func.now()) #(not implemented yet)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    Name = db.Column(db.String(150))
    notes = db.relationship("Note")




