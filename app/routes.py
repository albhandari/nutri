from crypt import methods
from wsgiref.util import request_uri
from bleach import ALLOWED_ATTRIBUTES

from requests import request
from app import appObj
from app.user_login import LoginUser

from app.create_account import CreateUser
from app.create_workout import CreateWorkout

from datetime import date

from app.delete_user import DeleteUser

from flask import render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from app import db
from app.models import User, Workout

from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required

import urllib.request

import os

#Justin
@appObj.route('/', methods = ['GET', 'POST'])
def login():
 login_form = LoginUser()
 if login_form.validate_on_submit():
  user = User.query.filter_by(username = login_form.username.data).first()
  if user != None:
   if user.check_password(login_form.password.data) == True:
    login_user(user)
    return redirect(url_for('home'))
   else:
    flash('Incorrect password. Please try again.')
  else:
   flash('Username does not exist. Please enter an existing username')
 return render_template('login.html', login_form = login_form)

#Justin
@appObj.route('/logout') #as of right now only included on home.html
def logout():
 logout_user() #from flask_login
 return redirect(url_for('login'))

#Justin
@appObj.route('/createAccount', methods = ['GET', 'POST'])
def createAccount():
  accountForm = CreateUser()
  if accountForm.validate_on_submit():
    same_name = User.query.filter_by(username = accountForm.username.data).first()
    if same_name == None:
      user=User()
      user.username=accountForm.username.data
      user.email=accountForm.email.data
      user.set_password(accountForm.password.data)
      user.weight = accountForm.weight.data
      user.fitness_goal = accountForm.fitness_goal.data
      user.user_bio = accountForm.user_bio.data
      #add to the database
      db.session.add(user)
      db.session.commit()
      #take the user back to login screen so they can log in with their new account
      flash('Your account has been created successfully')
      return redirect('/')
    else:
     flash('That username has been taken. Please try again')
  return render_template('create_account.html', accountForm = accountForm)

#Justin
@appObj.route('/deleteUser', methods = ['GET', 'POST'])
@login_required
#ADD DELETING MEALS, WORKOUTS 
def deleteAccount():
 account_form = DeleteUser()
 if account_form.validate_on_submit():
  user = User.query.filter_by(username = account_form.username.data).first()
  if user != None:
   if user.check_password(account_form.password.data) == True:
    u = User.query.filter_by(username = account_form.username.data)
    db.session.delete(user)
    db.session.commit()
    flash("Your account has been deleted successfully")
    return redirect('/') #after deleting account, redirect to login page
   else:
    flash("Please enter the correct password")
  else:
   flash("Please enter the correct username")
 return render_template('delete_user.html', accountForm = account_form)

#Justin
@appObj.route('/home') #home page
@login_required
def home():
 return render_template('home.html')


#Justin
@appObj.route('/createWorkout', methods = ['GET', 'POST'])
@login_required
def createWorkout():
 workout_form = CreateWorkout()
 if workout_form.validate_on_submit():
  creator = current_user
  workout = Workout()
  workout.name = workout_form.workout_name.data
  workout.exercise = workout_form.exercise.data
  workout.repititions = workout_form.repititions.data
  workout_day = workout_form.time_to_do.data #date from datetime type

  year = workout_day.year #get year
  month = workout_day.month #get month
  day = workout_day.day #get day
  workout.time_to_do = date(year, month, day) #set the day in the database

  workout.creator_id = creator.id #current user id

  #add to the database
  db.session.add(workout)
  db.session.commit()

  flash('Your workout has been created successfully')
 return render_template('create_workout.html', workout_form = workout_form)
