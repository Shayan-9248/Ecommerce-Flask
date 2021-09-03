from flask import Blueprint, render_template, redirect, request, session
from flask.helpers import url_for
from flask_login import current_user


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
def getCart():
    if 'Shoppingcart' not in session:
        return redirect(request.referrer)
    total_price = 0
    for key, product in session['Shoppingcart'].items():
        discount = (product['discount'] / 100) * float(product['price'])
        total_price += float(product['price']) * int(product['quantity'])
        total_price -= discount
        tax = ('%0.2f'% (0.6 * float(total_price)))
        grand_total = float('%0.2f'% (1.06 * total_price)) 
    return render_template('cart/detail.html', tax=tax, grand_total=grand_total)