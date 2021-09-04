from flask import (
    Blueprint, 
    render_template,
    request,
    flash,
    url_for,
    redirect,
)
from flask_paginate import get_page_parameter

from .models import Product, Category
from .forms import AddProduct

from app.extensions import db, search

blueprint = Blueprint('products', __name__)


@blueprint.get('/')
def index():
    page = request.args.get(get_page_parameter(), type=int, default=1)
    get_products = Product.query.filter_by(available=True).paginate(page=page, per_page=3)
    return render_template('product/index.html', get_products=get_products)


@blueprint.get('/result')
def result():
    searchWord = request.args.get('q')
    products = Product.query.msearch(searchWord, fields=['title', 'description'], limit=3)
    return render_template('product/result.html', products=products)


@blueprint.route('/<product_id>', methods=['get', 'post'])
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product/detail.html', product=product)


@blueprint.route('/add-product', methods=['get', 'post'])
def add_product():
    categories = Category.query.all()
    form = AddProduct()
    if form.validate_on_submit():
        product = Product(
            title=form.title.data,
            description=form.description.data,
            price=form.price.data,
            stock=form.stock.data,
            discount=form.discount.data,
            available=form.available.data,
            category_id=request.form.get('category'),
        )
        db.session.add(product)
        db.session.commit()
        flash(f'Product added successfully', 'success')
        return redirect(url_for('products.add_product'))
    return render_template('product/add.html', form=form, categories=categories)


# @blueprint.route('/add-cat', methods=['get', 'post'])
# def add_cat():
#     form = AddCategory()
#     if form.validate_on_submit():
#         cat = Category(
#             title=form.title.data
#         )
#         db.session.add(cat)
#         db.session.commit()
#         flash(f'Category added successfully', 'success')
#         return redirect(url_for('products.add_cat'))
#     return render_template('product/add_cat.html', form=form)