from app.models import User

from flask_wtf import FlaskForm, Form
from wtforms import StringField, PasswordField, SubmitField, \
    SelectField, DateField
from wtforms.validators import DataRequired, InputRequired, EqualTo, \
    ValidationError, Length


class LoginForm(FlaskForm):
    login = StringField("login", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("Войти")

    def validate_login(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user is None:
            raise ValidationError("Неверный логин")


class SignupForm(FlaskForm):
    firstname = StringField(
        "firstname",
        validators=[DataRequired()],
    )
    lastname = StringField(
        "lastname",
        validators=[DataRequired()],
    )
    login = StringField(
        "login",
        validators=[DataRequired()],
    )
    email = StringField(
        "Email",
        validators=[DataRequired()],
    )
    password = PasswordField(
        "password",
        validators=[DataRequired()],
    )
    confirmPassword = PasswordField(
        "confirmPassword",
        validators=[
            DataRequired(),
            EqualTo("password", message="Пароли должны совпадать"),
        ],
    )
    accountype = SelectField(
        "accountype",
        validators=[DataRequired()],
        choices=[
            ("Исполнитель", "Исполнитель"),
            ("Заказчик", "Заказчик"),
            ("Модератор", "Модератор"),
        ],
    )
    submit = SubmitField("Зарегистрироваться")

    def validate_login(self, login):
        user = User.query.filter_by(login=login.data).first()
        if user is not None:
            raise ValidationError("Этот логин уже занят")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Этот адрес электронной почты уже занят")


class TaskForm(FlaskForm):
    description = StringField(
        "description", validators=[DataRequired(), Length(max=20)]
    )
    comments = StringField("comments", validators=[DataRequired()])
    submit = SubmitField("Добавить")

class EditTaskForm(FlaskForm):
    status = SelectField(
        "status", 
        validators=[DataRequired()],
        choices=[
            ("Зарегистрирована", "Зарегистрирована"),
            ("Ожидает распределения", "Ожидает распределения"),
            ("Принята в работу", "Принята в работу"),
            ("Ожидает поставку", "Ожидает поставку"),
            ("Выполнена", "Выполнена")
        ]
    )
    deadline = DateField("deadline", validators=[InputRequired()])
    submit = SubmitField("Подтвердить изменения")

class EditTaskForm_mod(FlaskForm):
    status = SelectField(
        "status", 
        validators=[DataRequired()],
        choices=[
            ("Зарегистрирована", "Зарегистрирована"),
            ("Ожидает распределения", "Ожидает распределения"),
            ("Принята в работу", "Принята в работу"),
            ("Ожидает поставку", "Ожидает поставку"),
            ("Выполнена", "Выполнена")
        ]
    )
    submit = SubmitField("Подтвердить изменения")

class DeleteForm(FlaskForm):
    submit = SubmitField("Удалить задачу")

class TakeForm(FlaskForm):
    submit = SubmitField("Взять задачу")
    
