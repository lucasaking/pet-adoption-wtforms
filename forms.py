from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField
from wtforms.validators import InputRequired, Optional, URL
from wtforms.validators import ValidationError


def checkAge(form, field):
    if (field.data.lower() not in ['baby', 'young', 'adult', 'senior']):
        raise ValidationError('Must be baby, young, adult, or senior')


def checkSpecies(form, field):
    if (field.data.lower() not in ['cat', 'dog', 'porcupine']):
        raise ValidationError('Must be cat, dog, or porcupine')


class AddPetForm(FlaskForm):
    """Form for adding pets."""

    name = StringField("Pet Name", validators=[InputRequired()])
    species = StringField("Species", validators=[InputRequired(), checkSpecies])
    photo_url = StringField("Photo URL", validators=[URL(), Optional()])
    age = StringField("Age", validators=[InputRequired(), checkAge])
    notes = StringField("Additional Notes", validators=[Optional()])
    available = SelectField("Available", choices=[("True", 'Available'), ("False", 'Unavailable')],
        coerce=lambda x: x == 'True', validators=[InputRequired()])


class EditPetForm(FlaskForm):
    photo_url = StringField("Photo URL", validators=[URL(), Optional()])
    notes = StringField("Additional Notes", validators=[Optional()])
    available = SelectField("Available", choices=[('True', 'Available'), (
        'False', 'Unavailable')], coerce=lambda x: x == 'True', validators=[Optional()])
