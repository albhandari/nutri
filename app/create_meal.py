from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField, FloatField
from wtforms.validators import DataRequired, Length

class CreateMeal(FlaskForm):
    username = StringField('Username', validators = [DataRequired(),Length(min=3, max=32)], render_kw={"placeholder": "Ex: yofit, between 3 and 32 characters"})
    email = StringField ('Email', validators = [DataRequired()], render_kw={"placeholder": "Ex: yofit@gmail.com"})
    password = PasswordField( 'Password', validators = [DataRequired(), Length(min=4)], render_kw={"placeholder": "Minumum 4 characters"})
    weight = FloatField('Weight', validators = [DataRequired()], render_kw={"placeholder": "Ex: 100.5"})
    user_bio = StringField('Bio / Description', validators = [DataRequired(), Length(min = 3, max = 1024)], render_kw={"placeholder": "Tell us about yourself!"})
    fitness_goal = StringField('Fitness Goal', validators = [DataRequired(), Length(min = 3, max = 1024)], render_kw={"placeholder": "Tell us your fitness goal!"})
    submit = SubmitField('Create Account')
