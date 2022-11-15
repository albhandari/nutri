from app import db
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, date

#User table in the database
#A user has an id, username, email, and password hash
class User(UserMixin, db.Model):
 id = db.Column(db.Integer, primary_key = True)
 username = db.Column(db.String(16))
 email = db.Column(db.String(64))
 password_hash = db.Column(db.String(128))
 weight = db.Column(db.Float)
 fitness_goal = db.Column(db.String(1024))
 user_bio = db.Column(db.String(1024))

 #set user password
 def set_password(self, password):
  self.password_hash = generate_password_hash(password)

 #check user password 
 def check_password(self, password):
  return check_password_hash(self.password_hash, password)

#Meal table in the database
#Meal has id, name, type, ingredients, time to eat, and creator id
class Meal(db.Model):
 id = db.Column(db.Integer, primary_key = True)
 name = db.Column(db.String(32))
 meal_type = db.Column(db.String(16))
 meal_ingredients = db.Column(db.String(1024))
 time_to_eat = db.Column(db.DateTime(timezone = True))
 creator_id = db.Column(db.Integer, db.ForeignKey(User.id))

@login.user_loader
def load_user(id):
 return User.query.get(int(id))

class Workout(db.Model):
 id = db.Column(db.Integer, primary_key = True)
 name = db.Column(db.String(32))
 exercise = db.Column(db.String(32))
 repititions = db.Column(db.Integer)
 time_to_do = db.Column(db.Date, default = date.today())
 creator_id = db.Column(db.Integer, db.ForeignKey(User.id))
