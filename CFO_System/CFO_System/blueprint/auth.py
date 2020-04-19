from flask import render_template, flash, redirect, url_for, Blueprint
from flask_login import login_user, logout_user, login_required, current_user

from CFO_System.models import Administrator
from CFO_System.forms import LoginForm, RegisterForm
from CFO_System.utils import redirect_back
from CFO_System.models import User
from CFO_System.extensions import db

auth_bp = Blueprint("auth",__name__)


@auth_bp.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('customer.index')) # return to index if logged in

    form = LoginForm()
    if form.validate_on_submit():
        username = form.email.data
        password = form.password.data

        if username == 'admin':
            admin = Administrator.query.filter_by(administrator_name=username).first()
            if username == admin.administrator_name and admin.validate_password(password):
                login_user(admin)
                flash('Welcome back, admin.', 'info')
                return redirect(url_for('admin.index'))
            flash('Invalid username or password.', 'warning')
        else:
            user = User.query.filter_by(email=username).first()
            if user is not None and user.validate_password(form.password.data):
                login_user(user)
                flash('Login success.', 'info')
                return redirect_back()
            flash('Invalid email or password.', 'warning')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('customer.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data.lower()
        password = form.password.data
        user = User(email=email, user_name=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Register success!")
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout success.', 'info')
    return redirect(url_for('customer.index'))



