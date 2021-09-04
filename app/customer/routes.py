from flask import Blueprint, render_template

from .forms import CustomerRegisterForm


blueprint = Blueprint('customers', __name__)


@blueprint.route('/customer-register')
def customer_register():
    return render_template('customer/register.html')