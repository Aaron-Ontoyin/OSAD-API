from utils import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    firstname = db.Column(db.String(80), nullable=False, default='John')
    lastname = db.Column(db.String(80), nullable=False, default='Doe')
    phone = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    password = db.Column(db.String(128), nullable=False)
    remaining_requests = db.Column(db.Integer, nullable=False, default=-1)

    def __repr__(self):
        return '<User %r>' % self.username
