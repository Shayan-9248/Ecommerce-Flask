from app.extensions import db, admin
from app.database import BaseModel

from flask_admin.contrib.sqla import ModelView


class Product(BaseModel):
    __searchable__ = ['title', 'description']

    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(300))
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer)
    discount = db.Column(db.Integer, nullable=True)
    available = db.Column(db.Boolean, default=True)
    image = db.Column(db.LargeBinary, nullable=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='categories', lazy=True)

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.id}-{self.title})'


class Category(BaseModel):
    title = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.id}-{self.title})'


admin.add_view(ModelView(Product, db.session, url='admin-product'))
admin.add_view(ModelView(Category, db.session))