from app.extensions import db
from app.database import BaseModel

import json


class Order(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(40), nullable=False)
    country = db.Column(db.String(70), nullable=False)
    city = db.Column(db.String(90), nullable=False)
    address = db.Column(db.String(300), nullable=False)
    contact = db.Column(db.Integer, nullable=False)
    zip_code = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.id}-{self.user_id})'


class JsonEncodedDict(db.TypeDecorator):
    impl = db.Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    
    def process_result_param(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)


class OrderItem(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    quantity = db.Column(db.Integer, nullable=False)

    product = db.relationship('Product', backref='orderItem_product', lazy=True)
    order = db.relationship('Order', backref='orderItem_order', lazy=True)

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.id}-{self.user_id})'