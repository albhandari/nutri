from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, StringField
from wtforms.validators import DataRequired, Length, NumberRange
from wtforms.fields import DateField, TimeField


class AddFood(FlaskForm):
 name = StringField('Food Name', validators = [DataRequired(), Length(min=3, max=32)])
 calories = FloatField('Calorie Amount', validators = [DataRequired(), NumberRange(min = 0)])
 carbs = FloatField('Carbohydrate Amount (g)', validators = [DataRequired(), NumberRange(min = 0)])
 protien = FloatField('Protien Amount (g)', validators = [DataRequired(), NumberRange(min = 0)])
 fat = FloatField('Fat Amount (g)', validators = [DataRequired(), NumberRange(min = 0)])
 submit = SubmitField("Add to meal")

