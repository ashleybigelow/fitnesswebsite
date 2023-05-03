from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User, Workout
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import datetime
import json

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if user:
      if check_password_hash(user.password, password):
        flash("Logged in Successfully", category='success')
        login_user(user, remember=True)
        return(redirect(url_for('views.home')))
      else:
        flash("Incorrect Password", category='error')
    else:
      flash("Username Does Not Exist", category='error')

  return render_template("login.html", user = current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
  if request.method == "POST":
    email = request.form.get('email')
    username = request.form.get('username')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    user = User.query.filter_by(username=username).first()
    user2 = User.query.filter_by(email = email).first()
    if user:
      flash("Account with this username already exists", category='error')
    elif user2:
      flash("Account with this email already exists", category='error')
    elif len(email) < 4:
      flash("Email must be greater than 3 characters", category='error')
    elif len(username) < 4:
      flash("Username must be greater than 3 characters", category='error')
    elif password1 != password2:
      flash("Passwords must be the same", category='error')
    elif len(password1) < 7:
      flash("Password must be at least 7 characters", category='error')
    else:
      new_user = User(email = email, username = username, password = generate_password_hash(password1, method='sha256'))
      db.session.add(new_user)
      db.session.commit()
      flash("Account Created", category='success')
      user = User.query.filter_by(username=username).first()
      login_user(user, remember=True)
      return(redirect(url_for('views.home')))

  return render_template("sign-up.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
  flash("logout successful", category='success')
  logout_user()
  return redirect(url_for('auth.login'))

@auth.route('/settings', methods=['GET', 'POST'])
def settings():
  if request.method == 'POST':
    password = request.form.get('password')
    new_password = request.form.get('new_password')
    if password == new_password:
      flash("Entered password is the same as current password", category='error')
    elif check_password_hash(current_user.password, password):
      current_user.password = generate_password_hash(new_password, method='sha256')
      db.session.commit()
      flash("Password Updated", category='success')
    else:
      flash("Incorrect Password", category='error')
  return render_template("settings.html", user = current_user)

@auth.route('/fitness', methods=['GET', 'POST'])
def fitness():
  if request.method == 'POST':
    notes = request.form.get('notes')
    time = request.form.get('time')
    if request.values.get('distance'):
      distance = request.form.get('distance')
    else:
      distance = 0
    date = request.form.get('date')
    type = request.form.get('type')

    if request.values.get('distance'):
      if len(distance) < 1:
        flash("Must enter a Distance", category='error')
      elif not distance.replace('.','',1).isdigit():
        flash("Distance must be a number", category='error')

    if not time.isdecimal():
      flash("Time must be a number of minutes", category='error')
    elif not isValidDate(date):
      flash("The date must be a valid date in the form mm/dd/yyyy", category='error')
    elif not (len(date) == 10 or len(date) == 0):
      flash("The date must be a valid date in the form mm/dd/yyyy", category='error')
    else:
      flash("Workout Added", category='success')
      if len(date) == 0:
        new_workout = Workout(type = type, time = time, distance = distance, notes = notes, user_id=current_user.id)
      else :
        x = datetime.datetime(int(date[6:10]), int(date[0:2]), int(date[3:5]))
        new_workout = Workout(date = x, type = type, time = time, distance = distance, notes = notes, user_id=current_user.id)
    
      db.session.add(new_workout)
      db.session.commit()
  return render_template("fitness.html", user = current_user)

def isValidDate(date):
  if len(date) == 0:
    return True
  i = 0
  #check to make sure that numbers and slashes are in the right places
  for char in date:
    if i == 0 or i == 1 or i == 3 or i == 4 or i == 6 or i == 7 or i == 8 or i == 9:
      if not char.isdigit():
        return False
    else:
      if char != '/' and char !='-':
          return False
    i = i + 1
  #check to make sure that the year, day, and month are valid numbers
  if int(date[6:10]) < 1000:
    return False
  if int(date[0:2]) < 1 or int(date[0:2]) > 12:
    return False
  if int(date[3:5]) < 1 or int(date[3:5]) > 31:
    return False
  return True
      
@auth.route('/about')
def about():
  return render_template("about.html", user = current_user)

@auth.route('/meals')
def meals():
  return render_template("meals.html", user = current_user)

@auth.route('/history', methods=['GET', 'POST'])
def history():
  return render_template("history.html", user= current_user)

@auth.route('/edit/<int:id>', methods = ['GET', 'POST'])
def edit(id):
  if request.method == 'POST':
    type = request.form.get('type')
    date = request.form.get('date')
    time = request.form.get('time')
    distance = request.form.get('distance')
    notes = request.form.get('notes')

    #check to make sure the format of the date typed is valid
    if not isValidDate(date):
      flash("Please Enter a Valid Date in the Form mm/dd/yyyy", category='error')
    #if there are no errors, update the information and commit
    else:
      workout = Workout.query.get(id)      
      if len(type) > 0:
        workout.type = type
      if len(date) > 0:
        workout.date = datetime.datetime(int(date[6:10]), int(date[0:2]), int(date[3:5]))
      if len(time) > 0:
        workout.time = time
      if len(distance) > 0:
        workout.distance = distance
      if len(notes) > 0:
        workout.notes = notes
      db.session.commit()
      flash("Workout Successfully Updated", category='success')
      return(redirect(url_for('auth.history')))

  return render_template("edit.html", user = current_user)
