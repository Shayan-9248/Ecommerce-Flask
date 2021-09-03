from flask import Flask

from app.user.routes import blueprint as user_blueprint
from app.product.routes import blueprint as product_bluepinrt
from app.cart.routes import blueprint as cart_blueprint
from app.product.models import Product

from . import exceptions
from .extensions import db, migrate, bcrypt, login_manager, admin

import os


def register_blueprint(app):
    app.register_blueprint(user_blueprint)
    app.register_blueprint(product_bluepinrt)
    app.register_blueprint(cart_blueprint)


def register_error_handlers(e):
    app.register_error_handler(404, exceptions.page_not_found)
    app.register_error_handler(500, exceptions.server_error)


def register_shell_context(app):
    def shell_context():
        return {
            'db': db,
            'User': User,
            'Product': Product,
            # 'Cart': Cart
        }
    
    app.shell_context_processor(shell_context)

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
register_blueprint(app)
register_error_handlers(app)
register_shell_context(app)
app.config.from_object('config.DevConfig')


db.init_app(app)

from app.user.models import User # prevent to circular import
migrate.init_app(app, db)
bcrypt.init_app(app)
login_manager.init_app(app)
admin.init_app(app)