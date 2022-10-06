from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length

class CreateUser(FlaskForm):
    username = StringField('Username', validators = [DataRequired(),Length(min=3, max=32)], render_kw={"placeholder": "Ex: yofit, between 3 and 32 characters"})
    email = StringField ('Email', validators = [DataRequired()], render_kw={"placeholder": "Ex: yofit@gmail.com"})
    password = PasswordField( 'Password', validators = [DataRequired(), Length(min=4)], render_kw={"placeholder": "Minumum 4 characters"})
    submit = SubmitField('Create Account')
