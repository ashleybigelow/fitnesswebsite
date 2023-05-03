import uuid
from sqlalchemy.dialects.postgresql import UUID
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Workout(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  type = db.Column(db.String(150))
  time = db.Column(db.Integer)
  distance = db.Column(db.Float)
  date = db.Column(db.DateTime(timezone=True), default = func.now())
  notes = db.Column(db.String(150))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(150), unique = True)
  password = db.Column(db.String(150))
  username = db.Column(db.String(150), unique = True)
  workouts = db.relationship('Workout')