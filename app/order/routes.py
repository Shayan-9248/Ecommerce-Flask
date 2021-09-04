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

from .forms import OrderForm
from .models import Order, OrderItem

from app.extensions import db

blueprint = Blueprint('orders', __name__)


@blueprint.get('/order/<int:id>')
@login_required
def orderDetail(id):
    order = Order.query.get_or_404(id)
    return render_template('order/detail.html', order=order)


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
        return redirect(url_for('orders.orderDetail', order_id=order.id))
