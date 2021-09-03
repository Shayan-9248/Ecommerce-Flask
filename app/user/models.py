from app.extensions import db, login_manager
from app.database import BaseModel

from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(BaseModel, UserMixin):
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(70), unique=True, nullable=False)
    password = db.Column(db.String(120))

    def __repr__(self):
        return f'{self.__class__.__name__} ({self.id}-{self.username})'