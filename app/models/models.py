from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login_manager
from datetime import date, datetime

class User(UserMixin, db.Model):

    # user table
    __tablename__ = 'users'
    id = db.Column(db.Integer(), primary_key = True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(60), unique = True)
    password_hash = db.Column(db.String(120))
    business = db.relationship('Business', backref = 'business_owner', lazy = True)

    def __repr__(self):
        return f'User {self.username}'

    #password hashing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # compare password given is same as hashed password
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class Business(db.Model):

    # business table
    __tablename__ = 'businesses'
    id = db.Column(db.Integer(), primary_key = True)
    name = db.Column(db.String())
    location = db.Column(db.String())
    started = db.Column(db.DateTime(), default = datetime.utcnow)
    business_description = db.Column(db.String())
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __repr__(self):
        return f'Business name is {self.name}'
