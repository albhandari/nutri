from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields import DateField, TimeField
from wtforms.validators import DataRequired, Length

from datetime import date, time

class CreateWorkout(FlaskForm):
    workout_name = StringField('Workout Name', validators = [DataRequired(),Length(min=3, max=32)], render_kw={"placeholder": "Ex: yofit, between 3 and 32 characters"})
    exercise = StringField('Exercise', validators = [DataRequired(), Length(min=3, max=32)])
    repititions = IntegerField('Number of Repititions', validators = [DataRequired()])
    time_to_do = DateField('Day to do workout', format = '%Y-%m-%d', validators = [DataRequired()])
    time = TimeField('Time to do workout', format = '%H:%M', validators = [DataRequired()])
    submit = SubmitField('Save Workout')
