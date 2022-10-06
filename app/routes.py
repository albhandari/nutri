from crypt import methods
from wsgiref.util import request_uri
from bleach import ALLOWED_ATTRIBUTES

from requests import request
from app import appObj
from app.user_login import LoginUser


#from app.item_search import ItemSearch, SellerSearch
#from app.item_sale import SellItem
from app.createAccount import CreateUser

#from app.addToCart import addToCart, sessionCart, checkoutForm

#from app.user_rate_form import RateForm

#from app.delete_user import DeleteUser

#from app.addToCart import addToCart, sessionCart, checkoutForm

from flask import render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from app import db
from app.models import User

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

      #add to the database
      db.session.add(user)
      db.session.commit()
      #take the user back to login screen so they can log in with their new account
      flash('Your account has been created successfully')
      return redirect('/')
    else:
     flash('That username has been taken. Please try again')
  return render_template('createAccount.html', accountForm = accountForm)
