from crypt import methods
from wsgiref.util import request_uri


from app import appObj
from app.user_login import LoginUser

from app.create_account import CreateUser
from app.create_workout import CreateWorkout
from app.create_meal import CreateMeal
from app.add_nutrition import AddNutrition, DuplicateNutrition

from wtforms import SubmitField, FieldList

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
@appObj.route('/profile')
@login_required
def profile():
 user = current_user
 edit_profile = CreateUser()
 if edit_profile.validate_on_submit():
  user.username=accountForm.username.data
  user.email=accountForm.email.data
  user.set_password(accountForm.password.data)
  user.weight = accountForm.weight.data
  user.fitness_goal = accountForm.fitness_goal.data
  user.user_bio = accountForm.user_bio.data
  #add to the database
  db.session.add(user)
  db.session.commit()
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
  same_meal = Meal.query.filter_by(name = meal_form.meal_name.data).first()

  if same_meal != None:
   flash('You already have a meal with this name')
  else: #unique name
   meal = Meal()
   meal.name = meal_form.meal_name.data
   meal.type = request.form.get('meal_type') #get meal form from the html select attribute

   meal_item_names = meal_form.meal_item_names.data #list of foods
   item_names = ""
   for food in meal_item_names:
    item_names += food
    item_names += ", "

   meal.meal_item_names = item_names #convert list to string for db storage
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
   #add to the database
   db.session.add(meal)
   db.session.commit()
   return redirect('/addNutrition')
 return render_template('create_meal.html', meal_form = meal_form)

#Justin
#cannot add nutrition to more than one food because
#can't load more than one nutri form in the field list?
@appObj.route('/addNutrition', methods = ["GET", "POST"])
@login_required
def add_nutrition():
 user = current_user
 all_meals = Meal.query.filter_by(creator_id = user.id).all()
 current_meal = all_meals[-1] #last added meal = the meal the user just made
 initial_list = current_meal.meal_item_names.split(",") #list of all the food items
 food_list = []
 for food in initial_list:
  if food != ", " and food != " ":
   food_list.append(food)

 #for food in food_list:
 dup_nutrition_form = DuplicateNutrition() #needs a fieldlist for each food?
 if dup_nutrition_form.validate_on_submit():
  #adding inputted nutrition information
  for add_nutri in dup_nutrition_form.duplicate: 
   print(type(add_nutri))
   current_meal.meal_calories += add_nutri.food_calories.data
   current_meal.meal_carbs += add_nutri.food_carbs.data
   current_meal.meal_protien += add_nutri.food_protien.data
   current_meal.meal_fat += add_nutri.food_fat.data

  db.session.add(current_meal)
  db.session.commit()
  flash('Nutrition information has been added successfully')
 else:
  print('not valid')
 return render_template('add_nutrition.html', food_list = food_list, dup_nutrition_form = dup_nutrition_form)

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
 meal = Meal.query.filter_by(meal_name = meal_name).first()

#Justin
@appObj.route('/editWorkout/<workoutID>', methods = ["GET", "POST"])
@login_required
def edit_workout(workoutID):

 workout = Workout.query.filter_by(id = workoutID).first()
 if workout == None:
  print("???")
 workout_form = CreateWorkout()

 #make and save edits
 if workout_form.validate_on_submit():
  creator = current_user
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
 
 return render_template('edit_workout.html', workout_form = workout_form)

@appObj.route('/testing1')
def testing1():
  return render_template('testing.html');
