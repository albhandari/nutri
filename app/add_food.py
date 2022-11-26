from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, StringField
from wtforms.validators import DataRequired, Optional, Length
from wtforms.fields import DateField, TimeField


class AddFood(FlaskForm):
 name = StringField('Food Name', validators = [DataRequired(), Length(min=3, max=32)])
 calories = FloatField('Calorie Amount', validators = [DataRequired()],render_kw={"placeholder": "Enter a positive, non zero value"})
 carbs = FloatField('Carbohydrate Amount (g)', validators = [Optional()],render_kw={"placeholder": "Optional"})
 protien = FloatField('Protien Amount (g)', validators = [Optional()], render_kw={"placeholder": "Optional"})
 fat = FloatField('Fat Amount (g)', validators = [Optional()], render_kw={"placeholder": "Optional"})
 submit = SubmitField("Add to meal")

