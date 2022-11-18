from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, FieldList, FormField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateField, TimeField


class AddNutrition(FlaskForm):
 food_calories = FloatField('Calorie Amount', validators = [DataRequired()])
 food_carbs = FloatField('Carbohydrate Amount (g)', validators = [DataRequired()])
 food_protien = FloatField('Protien Amount (g)', validators = [DataRequired()])
 food_fat = FloatField('Fat Amount (g)', validators = [DataRequired()])

class DuplicateNutrition(FlaskForm):
 duplicate = FieldList(FormField(AddNutrition))
 submit = SubmitField("Save meal")
