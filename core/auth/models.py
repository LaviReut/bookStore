from .. import db
from werkzeug.security import generate_password_hash, check_password_hash
from .. import login
from flask_login import UserMixin
from ..models import Loans

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), index=True, unique=True)
    email = db.Column(db.String(), index=True, unique=True)
    age = db.Column(db.String())
    city = db.Column(db.String())
    password_hash = db.Column(db.String())
    loans = db.relationship('Loans', backref='user')
    imagePath = db.Column(db.String)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))