from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    role = db.Column(db.Enum('user', 'admin',
                     nullable=False, server_default='user', name='role_type'))
    password = db.Column(db.Text)

    def __init__(self, username, email, role):
        self.username = username
        self.email = email
        self.role = role

    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)
