from app import db
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#User table in the database
#A user has an id, username, email, and password hash
class User(UserMixin, db.Model):
 id = db.Column(db.Integer, primary_key = True)
 username = db.Column(db.String(16))
 email = db.Column(db.String(64))
 password_hash = db.Column(db.String(128))

 #set user password
 def set_password(self, password):
  self.password_hash = generate_password_hash(password)

 #check user password 
 def check_password(self, password):
  return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
 return User.query.get(int(id))

