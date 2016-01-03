from wtforms import Form, FloatField, validators
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask.ext.wtf import Form
from math import pi

class InputForm(Form):
    P = FileField('Das Bild', validators=[
      #  FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    S = FloatField(
        label='Felderanzahl', default=500,
        validators=[validators.InputRequired()])
    C = FloatField(
        label='Kompaktness', default=20,
        validators=[validators.InputRequired()])
    s = FloatField(
        label='Sigma', default=2,
        validators=[validators.InputRequired()])
    NC = FloatField(
        label='Anzahl der Farben', default=10,
        validators=[validators.InputRequired()])
