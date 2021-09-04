from wtforms import StringField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import (
    DataRequired,
)


class OrderForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    zip_code = StringField('ZipCode', validators=[DataRequired()])