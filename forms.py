from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from models import Movie
from email_validator import validate_email, EmailNotValidError  # Используем правильный импорт

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Регистрация')

class FeedbackForm(FlaskForm):
    rating = IntegerField('Рейтинг', validators=[DataRequired(), NumberRange(min=1, max=10)])
    message = TextAreaField('Сообщение', validators=[DataRequired()])
    movie_id = SelectField('Фильм', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Отправить')

    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.movie_id.choices = [(movie.id, movie.title) for movie in Movie.query.order_by(Movie.title).all()]

class SearchForm(FlaskForm):
    movie_title = StringField('Название фильма', validators=[DataRequired()])
    submit = SubmitField('Подобрать')
