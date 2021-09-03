from flask import (
    Blueprint, 
    render_template, 
    url_for, 
    redirect,
    flash,
    request,
)
from flask_login import (
    login_user, 
    logout_user, 
    current_user,
    login_required,
)

from .models import User
from .forms import UserSignUpForm, UserSignInForm
from app.extensions import db, bcrypt

blueprint = Blueprint('users', __name__)


@blueprint.route('/sign-up', methods=['post', 'get'])
def sign_up():
    if current_user.is_authenticated:
        flash('You are sign-up already', 'warning')
        return redirect(url_for('products.index'))
    form = UserSignUpForm()
    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=password
        )
        db.session.add(user)
        db.session.commit()
        flash('Signed-Up successfully', 'info')
        return redirect(url_for('products.index'))
    return render_template('user/sign_up.html', form=form)


@blueprint.route('/sign-in', methods=['post', 'get'])
def sign_in():
    if current_user.is_authenticated:
        flash('You are sign-in already', 'warning')
        return redirect(url_for('products.index'))
    form = UserSignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next', None)
            flash('Sign-In successfully', 'info')
            return redirect(next_page if next_page else url_for('products.index'))
        else:
            flash('Email or Password is incorrect', 'danger')
    return render_template('user/sign_in.html', form=form)


@blueprint.route('/sign-out')
@login_required
def sign_out():
    logout_user()
    flash('Sign-Out successfully', 'info')
    return redirect(url_for('products.index'))