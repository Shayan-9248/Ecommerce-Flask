from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import (
    DataRequired,
    Email,
)


class CustomerRegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    contact = StringField('Contact', validators=[DataRequired()])
    address = TextAreaField('Address', validators=[DataRequired()])
    zip_code = StringField('ZipCode', validators=[DataRequired()])
    submit = SubmitField('Register')