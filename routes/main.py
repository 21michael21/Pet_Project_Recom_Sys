from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from forms import LoginForm, RegistrationForm
from models import db, User
from routes import main_bp

@main_bp.route('/')
def home():
    return render_template('home.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Вы успешно вошли в систему.')
            return redirect(url_for('main_bp.home'))
        else:
            flash('Неверный email или пароль.')
    return render_template('login.html', form=form)

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно. Теперь вы можете войти.')
        return redirect(url_for('main_bp.login'))
    return render_template('register.html', form=form)

@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из системы.')
    return redirect(url_for('main_bp.home'))