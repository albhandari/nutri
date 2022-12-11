
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
from app.edit_workout import EditWorkout

from wtforms import SubmitField, FieldList

from datetime import date, time, datetime

from app.delete_user import DeleteUser

from flask import render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from app import db
from app.models import User, Workout, Meal

from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required

import urllib.request

import os

#login page 
@appObj.route('/', methods = ['GET', 'POST'])
def login():
 login_form = LoginUser()
 if login_form.validate_on_submit():
  user = User.query.filter_by(username = login_form.username.data).first() #first user with inputted username 
  if user != None:
   if user.check_password(login_form.password.data) == True: #login successful 
    login_user(user)
    return redirect(url_for('home'))
   else:
    flash('Incorrect password. Please try again.')
  else:
   flash('Username does not exist. Please enter an existing username')
 return render_template('login.html', login_form = login_form)

@appObj.route('/logout') 
def logout():
 logout_user() #from flask_login
 return redirect(url_for('login'))

#account registration 
@appObj.route('/createAccount', methods = ['GET', 'POST'])
def createAccount():
  accountForm = CreateUser()
  if accountForm.validate_on_submit():
    same_name = User.query.filter_by(username = accountForm.username.data).first() #check for duplicate username
    if same_name == None:
      #adding user to database 
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
     flash('That username has been taken. Please try again') #no duplicate usernames
  return render_template('create_account.html', accountForm = accountForm)

#deleting account 
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

#home page
@appObj.route('/home') 
@login_required
def home():
 user = current_user
 all_workouts = Workout.query.filter_by(creator_id = user.id).all()
 all_meals = Meal.query.filter_by(creator_id = user.id).all()
 return render_template('home.html', all_meals = all_meals, all_workouts = all_workouts)

#profile page 
@appObj.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
 user = current_user
 edit_profile = EditUser()
 if edit_profile.validate_on_submit():
  same_name = User.query.filter_by(username = edit_profile.username.data).first() #check for duplcate username after edit
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
  elif same_name != None and user.username == edit_profile.username.data: #did not change username
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
   
 #filling the intial form with user's current information
 edit_profile.username.data = user.username
 edit_profile.email.data = user.email
 edit_profile.weight.data = user.weight
 edit_profile.fitness_goal.data = user.fitness_goal
 edit_profile.user_bio.data = user.user_bio
 return render_template('user_profile.html', edit_profile = edit_profile)

#creating workout page 
@appObj.route('/createWorkout', methods = ['GET', 'POST'])
@login_required
def create_workout():
 workout_form = CreateWorkout()

 if workout_form.validate_on_submit():
  creator = current_user
  same_workout = Workout.query.filter_by(name = workout_form.workout_name.data, id = creator.id).first() #checking for duplicate workout with user id
  current_time = time(datetime.now().hour, datetime.now().minute)
  if same_workout != None:
   flash('You already have a workout with this name')
  elif workout_form.time_to_do.data < date.today(): #before today, not valid
   flash('Invalid date. Please try again')
  elif workout_form.time.data < current_time and workout_form.time_to_do.data == date.today(): #current day, but an earlier time 
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
   workout.time_workout = time(hour, minute) #set the time in the database

   workout.creator_id = creator.id #current user id

   #add to the database
   db.session.add(workout)
   db.session.commit()
   flash('Your workout has been created successfully')
 return render_template('create_workout.html', workout_form = workout_form)

#create meal page 
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
  elif meal_form.time.data < current_time and meal_form.time_to_eat.data == date.today(): #current day, but an earlier time 
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

   #initialize nutrition info to 0 before adding food information
   meal.meal_calories = 0
   meal.meal_carbs = 0
   meal.meal_protien = 0
   meal.meal_fat = 0

   #setting meal item names to empty string before adding food information 
   meal.meal_item_names = ""
   #add to the database
   db.session.add(meal)
   db.session.commit()
   flash('Your meal has been created successfully')
   return redirect('/home')
 return render_template('create_meal.html', meal_form = meal_form)

#add food page
@appObj.route('/addFoodExisting/<mealID>', methods = ["GET", "POST"])
@login_required
def add_food_existing(mealID):
 user = current_user
 current_meal = Meal.query.filter_by(id = mealID).first() #the meal with the specified id 
 food_form = AddFood()
 if food_form.validate_on_submit():
  for field in food_form:
   if field.data == None: #if the user did not input data for carbs, protien, or fat 
    field.data = 0

  #adding / calculating nutrition information
  if food_form.calories.data < 0 or food_form.carbs.data < 0 or food_form.protien.data < 0 or food_form.fat.data < 0: #no negative values
   flash('You cannot enter negative values. Please try again')
  else:
   #adding food information to the meal 
   current_meal.meal_item_names += food_form.name.data
   current_meal.meal_item_names += ", "
   current_meal.meal_calories += food_form.calories.data
   current_meal.meal_carbs += food_form.carbs.data
   current_meal.meal_protien += food_form.protien.data
   current_meal.meal_fat += food_form.fat.data
   #updating meal 
   db.session.add(current_meal)
   db.session.commit()
   flash('Food has been added to meal.')
   return redirect(request.referrer) #reload the page 
 return render_template('add_food.html', food_form = food_form)

#viewing meals page 
@appObj.route('/viewMeals')
@login_required
def view_meals():
 user = current_user
 all_meals = Meal.query.filter_by(creator_id = user.id).all() #all the meals the user has created 
 current = 0;
 total_calories = 0;
 total_carbs = 0;
 total_protein = 0;
 total_fat = 0;


 #gathers meal values for the 3 most recently added meals 
 for meal in all_meals:
  if(current < 3):
    total_calories = total_calories + meal.meal_calories
    total_carbs = total_carbs + meal.meal_carbs
    total_protein = total_protein + meal.meal_protien
    total_fat = total_fat + meal.meal_fat
    current = current +1
  else:
    break
  
  calPer = (total_calories/2500) * 100
  carPer = (total_carbs / 1250) * 100
  proPer = (total_protein / 80) * 100
  fatPer = (total_fat / 97) * 100

 return render_template('view_meals.html',fatPer = fatPer,proPer = proPer,carPer = carPer ,calPer = calPer, all_meals = all_meals, cal= total_calories, carb = total_carbs, pro= total_protein, fat = total_fat)


#viewing workouts page
@appObj.route('/viewWorkouts')
@login_required
def view_workouts():
 user = current_user
 all_workouts = Workout.query.filter_by(creator_id = user.id).all() #all workouts created by user
 current = 0;
 wo1 = "";
 wo2 = "";
 wo3 = "";

 rep1 = 0;
 rep2 = 0;
 rep3 = 0;

 per1 = 0;
 per2 = 0;
 per3 = 0;

 total = 0;

 #lists workout values for the past 3 workouts
 for workout in all_workouts:
  if(current < 3):
    if(current == 0):
      wo1 = workout.exercise
      rep1 = workout.repititions
      total = total + rep1
    elif(current == 1):
      wo2 = workout.exercise
      rep2 = workout.repititions
      total = total + rep2
    elif(current == 2):
      wo3 = workout.exercise
      rep3 = workout.repititions
      total = total + rep3
    
    current = current + 1;
  else:
    break
  
  total = rep1 + rep2 + rep3

  per1 = (((rep1 / total)) * 100)
  per2 = ((rep2 / total) * 100)
  per3 = ((rep3 / total) * 100)


    

 return render_template('view_workouts.html', all_workouts = all_workouts, wo1= wo1, wo2 = wo2, wo3 = wo3, rep1 = rep1, rep2 = rep2, rep3 = rep3, per1 = per1, per2 = per2, per3 = per3)

#edit meal page 
@appObj.route('/editMeal/<mealID>', methods = ["GET", "POST"])
@login_required
def edit_meal(mealID):
 creator = current_user
 meal = Meal.query.filter_by(id = mealID).first()
 meal_form = EditMeal()
 if meal_form.validate_on_submit():
  if meal_form.time_to_eat.data < date.today(): #before current day, not valid
   flash('Invalid date. Please try again')
  elif meal_form.time.data < time(datetime.now().hour, datetime.now().minute) and meal_form.time_to_eat.data == date.today(): #current day, earlier time
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
 
 #getting the original day to eat meal
 original_meal_day = meal.time_to_eat 
 original_meal_year = original_meal_day.year
 original_meal_month = original_meal_day.month
 original_meal_number_day = original_meal_day.day

 #getting the original time to eat meal
 original_meal_time = meal.time_meal
 original_meal_hour = original_meal_time.hour
 original_meal_minute = original_meal_time.minute

 meal_form.time_to_eat.data = date(original_meal_year, original_meal_month, original_meal_number_day)
 meal_form.time.data = time(original_meal_hour, original_meal_minute)
 return render_template('edit_meal.html', meal_form = meal_form, meal = meal)

#edit workout page 
@appObj.route('/editWorkout/<workoutID>', methods = ["GET", "POST"])
@login_required
def edit_workout(workoutID):

 workout = Workout.query.filter_by(id = workoutID).first()
 workout_form = EditWorkout()

 #make and save edits
 if workout_form.validate_on_submit():
  if workout_form.time_to_do.data < date.today(): #before today, not valid
   flash('Invalid date. Please try again')
  elif workout_form.time.data < time(datetime.now().hour, datetime.now().minute) and workout_form.time_to_do.data == date.today(): #current day, earlier time
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
 
 #getting original day and time to do workout
 original_workout_day = workout.time_to_do
 original_workout_year = original_workout_day.year
 original_workout_month = original_workout_day.month
 original_workout_number_day = original_workout_day.day
 
 original_workout_time = workout.time_workout
 original_workout_hour = original_workout_time.hour
 original_workout_minute = original_workout_time.minute

 #create workout form whose values are already the workout values
 workout_form.exercise.data = workout.exercise
 workout_form.repititions.data = workout.repititions
 workout_form.time_to_do.data = date(original_workout_year, original_workout_month, original_workout_number_day)
 workout_form.time.data = time(original_workout_hour, original_workout_minute)
 
 return render_template('edit_workout.html', workout_form = workout_form, workout = workout)

