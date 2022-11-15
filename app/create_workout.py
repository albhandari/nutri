
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Length

from datetime import date

class CreateWorkout(FlaskForm):
    workout_name = StringField('Workout Name', validators = [DataRequired(),Length(min=3, max=32)])
    exercise = StringField('Exercise', validators = [DataRequired(), Length(min=3, max=32)])
    repititions = IntegerField('Number of Repititions', validators = [DataRequired()])
    time_to_do = DateField('Time to do workout', format = '%Y-%m-%d', validators = [DataRequired()])
    submit = SubmitField('Create Workout')
