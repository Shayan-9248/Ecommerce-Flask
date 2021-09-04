from flask import (
    Blueprint, 
    render_template, 
    flash, 
    redirect,
    url_for,
    request,
    session,
)
from flask_login import login_required, current_user
from decouple import config

from .forms import OrderForm
from .models import Order, OrderItem

from app.extensions import db
import stripe

blueprint = Blueprint('orders', __name__)

publishable_key = config('publishable_key')

stripe.api_key = config('stripe.api_key')

@blueprint.post('/payment')
@login_required
def payment():
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken'],
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        description='Myshop',
        amount=500,
        currency='usd',
    )
    orders = OrderItem.query.filter_by(user_id=current_user.id).order_by(
        OrderItem.id.desc()).first()
    return redirect(url_for('orders.thank'))


@blueprint.get('/payment-success')
def thank():
    return render_template('order/thank.html')


@blueprint.get('/order/<int:id>')
@login_required
def orderDetail(id):
    orders = OrderItem.query.filter_by(id=id).order_by(OrderItem.id.desc()).first()
    total_price = 0
    grand_price = 0
    for key, item in session['Shoppingcart'].items():
        discount = (item['discount'] / 100) * float(item['price'])
        total_price += float(item['price']) * int(item['quantity'])
        total_price -= discount
        tax = ('%0.2f'% (0.6 * float(total_price)))
        grand_total = ('%0.2f'% (1.06 * float(total_price)))
    return render_template('order/detail.html', orders=orders, grand_total=grand_total)


@blueprint.post('/order')
@login_required
def createOrder():
    if request.method == 'POST':
        form = OrderForm()
        if form.validate_on_submit():
            order = Order(
                user_id=current_user.id,
                name=form.name.data,
                country=form.country.data,
                city=form.city.data,
                address=form.address.data,
                contact=form.contact.data,
                zip_code=form.zip_code.data
            )
            db.session.add(order)
            db.session.commit()
        for key, item in session['Shoppingcart'].items():
            orderItem = OrderItem(
                order_id=order.id,
                user_id=current_user.id, 
                product_id=key, 
                quantity=item['quantity']
            )
            db.session.add(orderItem)
            db.session.commit()
            flash('Order created successfully', 'success')
        return redirect(url_for('orders.orderDetail', id=order.id))
