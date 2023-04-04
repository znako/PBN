from app import db, login

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(120), unique=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    accountype = db.Column(db.Integer)

    def is_executor(self):
        if self.accountype == 0:
            return True
        return False

    def is_consumer(self):
        if self.accountype == 1:
            return True
        return False

    def is_moderator(self):
        if self.accountype == 2:
            return True
        return False

    def get_accountype(self):
        if self.accountype == 0:
            return "Исполнитель"

        if self.accountype == 1:
            return "Заказчик"

        if self.accountype == 2:
            return "Модератор"

    def __repr__(self):
        return "<User {}>".format(self.login)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_accountype(self, input_accountype):
        if input_accountype == "Исполнитель":
            self.accountype = 0

        if input_accountype == "Заказчик":
            self.accountype = 1

        if input_accountype == "Модератор":
            self.accountype = 2


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class ActiveTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(64))
    executor_login = db.Column(db.String(64))
    consumer_login = db.Column(db.String(64))
    deadline = db.Column(db.String(64))
    description = db.Column(db.String(32))
    comments = db.Column(db.String(256))
    is_archived = db.Column(db.Boolean)

    def __repr__(self):
        return "<Table {}>".format(self.id)
    