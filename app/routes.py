from crypt import methods
from wsgiref.util import request_uri


from app import appObj
from app.user_login import LoginUser

from app.create_account import CreateUser
from app.create_workout import CreateWorkout
from app.create_meal import CreateMeal

from datetime import date, time

from app.delete_user import DeleteUser

from flask import render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from app import db
from app.models import User, Workout, Meal

from app.add_to_meal import MealAdd

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

    #delete meals the user created
    meals = Meal.query.filter_by(creator_id = user.id).all()
    for m in meals:
     db.session.delete(m)
     db.session.commit()

    #delete workouts the user created
    workouts = Workout.query.filter_by(creator_id = user.id).all()
    for w in workouts:
     db.session.delete(w)
     db.session.commit()

    #delete user
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
  workout_time = workout_form.time.data #time 


  year = workout_day.year #get year
  month = workout_day.month #get month
  day = workout_day.day #get day
  workout.time_to_do = date(year, month, day) #set the day in the database

  hour = workout_time.hour
  minute = workout_time.minute
  workout.time_workout = time(hour, minute)

  workout.creator_id = creator.id #current user id

  #add to the database
  db.session.add(workout)
  db.session.commit()

  flash('Your workout has been created successfully')
 return render_template('create_workout.html', workout_form = workout_form)


#Justin
@appObj.route('/createMeal', methods = ['GET', 'POST'])
@login_required
def createMeal():
 meal_form = CreateMeal()

 if meal_form.validate_on_submit():
  creator = current_user
  meal = Meal()
  meal.name = meal_form.meal_name.data
  meal.type = request.form.get('meal_type') #get meal form from the html select attribute
  meal_item_names = meal_form.meal_item_names.data #list of foods
  meal.meal_item_names = ", ".join(meal_item_names) #convert list to string for db storage
  meal_day = meal_form.time_to_eat.data #date from datetime type
  meal_time = meal_form.time.data

  year = meal_day.year #get year
  month = meal_day.month #get month
  day = meal_day.day #get day
  meal.time_to_eat = date(year, month, day) #set the day in the database

  hour = meal_time.hour
  minute = meal_time.minute
  meal.time_meal = time(hour, minute)

  meal.creator_id = creator.id #current user id

  #add to the database
  db.session.add(meal)
  db.session.commit()

  flash('Your meal has been created successfully')

 return render_template('create_meal.html', meal_form = meal_form)


@appObj.route('/testing1')
def testing1():
  return render_template('testing.html');