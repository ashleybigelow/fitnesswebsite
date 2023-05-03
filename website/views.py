from unicodedata import category
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import current_user
import json
from . import db
from .models import Workout

views = Blueprint('views', __name__)

@views.route('/')
def home():
  return render_template("home.html", user = current_user)

@views.route('/delete-workout', methods=['POST'])
def delete_workout():
  workout = json.loads(request.data)
  workoutId = workout['workoutId']
  workout = Workout.query.get(workoutId)
  if workout:
    if workout.user_id == current_user.id:
      db.session.delete(workout)
      db.session.commit()
  return jsonify({})

@views.route('/delete-acct', methods=['POST'])
def delete_acct():
  db.session.delete(current_user)
  db.session.commit()
  return redirect(url_for('auth.home'))