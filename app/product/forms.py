from flask_wtf import FlaskForm
from flask_wtf.file import (
    FileField, 
    FileRequired,
    FileAllowed,
)
from wtforms import (
    StringField, 
    BooleanField, 
    TextAreaField,
    IntegerField,
)
from wtforms.validators import DataRequired, ValidationError

from .models import Category, Product


class AddProduct(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    price = IntegerField('Price', validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired()])
    discount = IntegerField('Discount', default=0)
    available = BooleanField('Available')
    image = FileField('Image')

    def validate_title(self, title):
        product = Product.query.filter_by(title=title.data).first()
        if product:
            raise ValidationError(f'Product with this title already exists.')


class AddCategory(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])

    def validate_title(self, title):
        cat = Category.query.filter_by(title=title.data).first()
        if cat:
            raise ValidationError(f'Category with this title already exists.')