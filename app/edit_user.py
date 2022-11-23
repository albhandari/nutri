
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, FloatField
from wtforms.validators import DataRequired, Length

class EditUser(FlaskForm):
    username = StringField('Username', validators = [DataRequired(),Length(min=3, max=32)])
    email = StringField ('Email', validators = [DataRequired()])
    weight = FloatField('Weight', validators = [DataRequired()])
    user_bio = StringField('Bio / Description', validators = [DataRequired(), Length(min = 3, max = 1024)])
    fitness_goal = StringField('Fitness Goal', validators = [DataRequired(), Length(min = 3, max = 1024)])
    submit = SubmitField('Save Information')
