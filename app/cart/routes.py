from flask import (
    Blueprint, 
    render_template, 
    redirect, 
    request, 
    session,
    flash,
)
from flask.helpers import url_for
from flask_login import login_required


from app.product.models import Product
from app.extensions import db

blueprint = Blueprint('carts', __name__)


def MagerDict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@blueprint.route('/add-cart', methods=['post'])
@login_required
def add_cart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        product = Product.query.filter_by(id=product_id).first()
        if product_id and quantity and request.method == 'POST':
            dictItems = {
                product_id: {
                    'title': product.title,
                    'price': product.price,
                    'discount': product.discount,
                    'quantity': quantity
                    }
                }
            if 'Shoppingcart' in session:
                print(session['Shoppingcart'])
                if product_id in session['Shoppingcart']:
                    print('This product already is in your cart')
                else:
                    session['Shoppingcart'] = MagerDict(session['Shoppingcart'], dictItems)
                    return redirect(request.referrer)
            else:
                session['Shoppingcart'] = dictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)


@blueprint.route('/carts')
@login_required
def getCart():
    if 'Shoppingcart' not in session or len(session['Shoppingcart']) <= 0:
        return redirect(url_for('products.index'))
    total_price = 0
    grand_total = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount'] / 100) * float(product['price'])
        total_price += float(product['price']) * int(product['quantity'])
        total_price -= discount
        tax = ('%0.2f'% (0.6 * float(total_price)))
        grand_total = float('%0.2f'% (1.06 * total_price)) 
    return render_template('cart/detail.html', grand_total=grand_total, tax=tax)


@blueprint.post('/update-cart/<int:id>')
@login_required
def updateCart(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('products.index'))
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        try:
            session.modified = True
            for key, item in session['Shoppingcart'].items():
                if int(key) == id:
                    item['quantity'] = quantity
                    flash('Item updated successfully', 'success')
                    return redirect(url_for('carts.getCart'))
        except Exception as e:
            return redirect(url_for('carts.getCart'))


@blueprint.route('/delete-cart/<int:id>')
@login_required
def deleteCart(id):
    if 'Shoppingcart' not in session and len(session['Shoppingcart']) <= 0:
        return redirect(url_for('products.index'))
    try:
        session.modified = True
        for key, item in session['Shoppingcart'].items():
            if int(key) == id:
                session['Shoppingcart'].pop(key, None)
                return redirect(url_for('carts.getCart'))
    except Exception as e:
            return redirect(url_for('carts.getCart'))