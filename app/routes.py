
from crypt import methods
from wsgiref.util import request_uri


from app import appObj
from app.user_login import LoginUser

from app.create_account import CreateUser
from app.create_workout import CreateWorkout
from app.create_meal import CreateMeal
from app.edit_meal import EditMeal
from app.edit_user import EditUser
from app.add_food import AddFood

from wtforms import SubmitField, FieldList

from datetime import date, time, datetime

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
@appObj.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
 user = current_user
 edit_profile = EditUser()
 if edit_profile.validate_on_submit():
  same_name = User.query.filter_by(username = edit_profile.username.data).first()
  if same_name == None:
   user.username=edit_profile.username.data
   user.email=edit_profile.email.data
   user.weight = edit_profile.weight.data
   user.fitness_goal = edit_profile.fitness_goal.data
   user.user_bio = edit_profile.user_bio.data
   #add to the database
   db.session.add(user)
   db.session.commit()
   flash ('Your information has been updated successfully')
  else:
   flash('That username already exists. Please try again')

 edit_profile.username.data = user.username
 edit_profile.email.data = user.email
 edit_profile.weight.data = user.weight
 edit_profile.fitness_goal.data = user.fitness_goal
 edit_profile.user_bio.data = user.user_bio
 return render_template('user_profile.html', edit_profile = edit_profile)

#Justin
@appObj.route('/createWorkout', methods = ['GET', 'POST'])
@login_required
def create_workout():
 workout_form = CreateWorkout()

 if workout_form.validate_on_submit():
  creator = current_user
  same_workout = Workout.query.filter_by(name = workout_form.workout_name.data, id = creator.id).first()
  current_time = time(datetime.now().hour, datetime.now().minute)
  if same_workout != None:
   flash('You already have a workout with this name')
  elif workout_form.time_to_do.data < date.today(): #before today, not valid
   flash('Invalid date. Please try again')
  elif workout_form.time.data < current_time and workout_form.time_to_do.data == date.today():
   flash('Invalid time. Please try again')
  else: #unique name

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
def create_meal():
 creator = current_user
 meal_form = CreateMeal()

 if meal_form.validate_on_submit():
  creator = current_user
  same_meal = Meal.query.filter_by(name = meal_form.meal_name.data, id = creator.id).first()
  current_time = time(datetime.now().hour, datetime.now().minute)
  if same_meal != None:
   flash('You already have a meal with this name')
  elif meal_form.time_to_eat.data < date.today(): #before today, not valid
   flash('Invalid date. Please try again')
  elif meal_form.time.data < current_time and meal_form.time_to_eat.data == date.today():
   flash('Invalid time. Please try again')
  else: #unique name
   meal = Meal()
   meal.name = meal_form.meal_name.data
   meal.type = request.form.get('meal_type') #get meal form from the html select attribute

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

   #initialize nutrition info to 0 before adding information
   meal.meal_calories = 0
   meal.meal_carbs = 0
   meal.meal_protien = 0
   meal.meal_fat = 0

   meal.meal_item_names = ""
   #add to the database
   db.session.add(meal)
   db.session.commit()
   return redirect('/addFood')
 return render_template('create_meal.html', meal_form = meal_form)

#Justin
#cannot add nutrition to more than one food because
#can't load more than one nutri form in the field list?
@appObj.route('/addFood', methods = ["GET", "POST"])
@login_required
def add_food():
 user = current_user
 all_meals = Meal.query.filter_by(creator_id = user.id).all()
 current_meal = all_meals[-1] #last added meal = the meal the user just made
 food_form = AddFood()
 if food_form.validate_on_submit():
  current_meal.meal_item_names += food_form.name.data
  current_meal.meal_item_names += ", "
  current_meal.meal_calories += food_form.calories.data
  current_meal.meal_carbs += food_form.carbs.data
  current_meal.meal_protien += food_form.protien.data
  current_meal.meal_fat += food_form.fat.data
  db.session.add(current_meal)
  db.session.commit()
  flash('Food has been added to meal.')
  return redirect(request.referrer)
 return render_template('add_food.html', food_form = food_form)

#Justin
@appObj.route('/viewMeals')
@login_required
def view_meals():
 user = current_user
 all_meals = Meal.query.filter_by(creator_id = user.id).all()
 return render_template('view_meals.html', all_meals = all_meals)


#Justin
@appObj.route('/viewWorkouts')
@login_required
def view_workouts():
 user = current_user
 all_workouts = Workout.query.filter_by(creator_id = user.id).all()
 return render_template('view_workouts.html', all_workouts = all_workouts)

#Justin
@appObj.route('/editMeal/<meal_name>', methods = ["GET", "POST"])
@login_required
def edit_meal(meal_name):
 creator = current_user
 meal = Meal.query.filter_by(name = meal_name).first()
 meal_form = EditMeal()
 if meal_form.validate_on_submit():
  if meal_form.time_to_eat.data < date.today(): #before today, not valid
   flash('Invalid date. Please try again')
  elif meal_form.time.data < time(datetime.now().hour, datetime.now().minute) and meal_form_time_to_eat.data == date.today():
   flash('Invalid time. Please try again')
  else:
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
   flash('Your meal has been saved successfully') 

 original_meal_day = meal.time_to_eat
 original_meal_year = original_meal_day.year
 original_meal_month = original_meal_day.month
 original_meal_number_day = original_meal_day.day

 original_meal_time = meal.time_meal
 original_meal_hour = original_meal_time.hour
 original_meal_minute = original_meal_time.minute

 meal_form.time_to_eat.data = date(original_meal_year, original_meal_month, original_meal_number_day)
 meal_form.time.data = time(original_meal_hour, original_meal_minute)
 return render_template('edit_meal.html', meal_form = meal_form, meal = meal)

#Justin
@appObj.route('/editWorkout/<workoutID>', methods = ["GET", "POST"])
@login_required
def edit_workout(workoutID):

 workout = Workout.query.filter_by(id = workoutID).first()
 workout_form = CreateWorkout()

 #make and save edits
 if workout_form.validate_on_submit():
  if workout_form.time_to_do.data < date.today(): #before today, not valid
   flash('Invalid date. Please try again')
  elif workout_form.time.data < time(datetime.now().hour, datetime.now().minute) and workout_form.time_to_data == date.today():
   flash('Invalid time. Please try again')
  else:
   creator = current_user
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
   flash('Your workout has been saved successfully')
 
 original_workout_day = workout.time_to_do
 original_workout_year = original_workout_day.year
 original_workout_month = original_workout_day.month
 original_workout_number_day = original_workout_day.day
 original_workout_time = workout.time_workout
 original_workout_hour = original_workout_time.hour
 original_workout_minute = original_workout_time.minute

 #create workout form whose values are already the workout values
 workout_form.workout_name.data = workout.name
 workout_form.exercise.data = workout.exercise
 workout_form.repititions.data = workout.repititions
 workout_form.time_to_do.data = date(original_workout_year, original_workout_month, original_workout_number_day)
 workout_form.time.data = time(original_workout_hour, original_workout_minute)
 
 return render_template('edit_workout.html', workout_form = workout_form, workout = workout)

@appObj.route('/testing1')
def testing1():
  return render_template('testing.html');
