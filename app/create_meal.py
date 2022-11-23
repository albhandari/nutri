from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SubmitField, FormField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateField, TimeField

from datetime import date, time

class CreateMeal(FlaskForm):
 meal_name = StringField('Meal Name', validators = [DataRequired(), Length(min = 3, max = 32)])
 time_to_eat = DateField('Day to eat meal', format = '%Y-%m-%d', validators = [DataRequired()])
 time = TimeField('Time to eat meal', format = '%H:%M', validators = [DataRequired()])
 submit = SubmitField('Save Meal')
