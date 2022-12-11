from flask_wtf import FlaskForm
from wtforms import StringField, FieldList, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length
from wtforms.fields import DateField, TimeField

from datetime import date, time

class EditWorkout(FlaskForm):
 exercise = StringField('Exercise', validators = [DataRequired(), Length(min=3, max=32)], render_kw={"placeholder": "Ex: yoFit, betwene 3 and 32 characters"})
 repititions = IntegerField('Number of Repititions', validators = [DataRequired()])
 time_to_do = DateField('Day to eat meal', format = '%Y-%m-%d', validators = [DataRequired()])
 time = TimeField('Time to eat meal', format = '%H:%M', validators = [DataRequired()])
 submit = SubmitField('Save Workout')
