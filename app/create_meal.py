from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SubmitField, FormField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateField

from datetime import date

class CreateMeal(FlaskForm):
 meal_name = StringField('Meal Name', validators = [DataRequired(), Length(min = 3, max = 32)])
 meal_item_names = FieldList(StringField('Food Name', validators = [DataRequired(), Length(min = 3, max = 32)]), min_entries = 1, max_entries = 10)
 time_to_eat = DateField('Time to eat meal', format = '%Y-%m-%d', validators = [DataRequired()])
 submit = SubmitField('Create Meal')
