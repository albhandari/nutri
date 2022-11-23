from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, StringField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateField, TimeField


class AddFood(FlaskForm):
 name = StringField('Food Name', validators = [DataRequired(), Length(min=3, max=32)])
 calories = FloatField('Calorie Amount', validators = [DataRequired()])
 carbs = FloatField('Carbohydrate Amount (g)', validators = [DataRequired()])
 protien = FloatField('Protien Amount (g)', validators = [DataRequired()])
 fat = FloatField('Fat Amount (g)', validators = [DataRequired()])
 submit = SubmitField("Add to meal")

