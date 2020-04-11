# -*- coding: utf-8 -*-

import click # only for debug
from flask import flash, redirect, url_for, render_template, session, abort

from customer_system import app, db
from customer_system.forms import LoginForm, LogoutForm, RegisterForm, PasswordForm, NameForm, ContactForm, DepositForm, WithdrawForm
from customer_system.models import User


@app.route('/')
def re():
    return redirect(url_for('index'))


@app.route('/index/', methods=['GET', 'POST'])
def index():
    '''Display the index page'''
    welcome = 'Welcome!'
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        welcome += ' ID: {} Name: {}'.format(user.user_id, user.user_name)
    logout_form = LogoutForm()
    if logout_form.submit_logout.data and logout_form.validate_on_submit():
        if 'user_id' in session:
            session.pop('user_id')
            flash('You have successfully signed out!')
        return redirect(url_for('index'))
    return render_template('index.html', welcome=welcome, logout_form=logout_form)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    '''Display the login form and set cookie if login succeeds'''
    login_form = LoginForm()
    if login_form.submit.data and login_form.validate_on_submit():
        email = login_form.email.data
        user_password = login_form.user_password.data
        result = User.query.filter(User.email==email, User.user_password==user_password).all()
        if len(result) > 1:
            abort(500)
        if result:
            session['user_id'] = result[0].user_id
            flash('You have successfully signed in!')
            return redirect(url_for('index'))
        flash('Account does not exist or password is wrong!')
        return redirect(url_for('login'))
    return render_template('login.html', login_form=login_form)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    '''Display the register form and check for duplications'''
    register_form = RegisterForm()
    if register_form.submit.data and register_form.validate_on_submit():
        email = register_form.email.data
        user_password = register_form.user_password.data
        result = User.query.filter(User.email==email).all()
        if result:
            flash('The email address has already been registered!')
            return redirect(url_for('register'))
        user = User(
            email = email,
            user_password = user_password,
            user_name = 'Unnamed User',
            user_avatar = None,
            user_contact = '',
            available_balance = 0,
            frozen_balance = 0,
            user_status = 'normal'
        )
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered!')
        return redirect(url_for('index'))
    return render_template('register.html', register_form=register_form)


@app.route('/personal_center/', methods=['GET', 'POST'])
def personal_center():
    '''Check login status and display the forms in the personal center page'''
    if 'user_id' not in session:
        abort(404)
    user = User.query.get(session['user_id'])

    password_form = PasswordForm()
    name_form = NameForm()
    contact_form = ContactForm()
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()

    if password_form.submit_password.data and password_form.validate_on_submit():
        user.user_password = password_form.user_password.data
        db.session.commit()
        flash('You have successfully changed your password!')
        return redirect(url_for('personal_center'))

    if name_form.submit_name.data and name_form.validate_on_submit():
        user.user_name = name_form.user_name.data
        db.session.commit()
        flash('You have successfully changed your name!')
        return redirect(url_for('personal_center'))

    if contact_form.submit_contact.data and contact_form.validate_on_submit():
        user.user_contact = contact_form.user_contact.data
        db.session.commit()
        flash('You have successfully changed your contact!')
        return redirect(url_for('personal_center'))

    if deposit_form.submit_deposit.data and deposit_form.validate_on_submit():
        amount = round(deposit_form.deposit_amount.data, 2)
        if user.available_balance + amount <= 10000:
            user.available_balance = round(user.available_balance + amount, 2)
            db.session.commit()
            flash('You have successfully deposited {}!'.format(amount))
        else:
            flash('Exceed maximum balance limit!')
        return redirect(url_for('personal_center'))

    if withdraw_form.submit_withdraw.data and withdraw_form.validate_on_submit():
        amount = round(withdraw_form.withdraw_amount.data, 2)
        if user.available_balance - amount >= 0:
            user.available_balance = round(user.available_balance - amount, 2)
            db.session.commit()
            flash('You have successfully withdrew {}!'.format(amount))
        else:
            flash('Insufficient funds!')
        return redirect(url_for('personal_center'))

    name_form.user_name.data = user.user_name
    contact_form.user_contact.data = user.user_contact
    return render_template('personal_center.html', user_id=user.user_id, email=user.email,
        password_form=password_form, name_form=name_form, contact_form=contact_form,
        available_balance=user.available_balance, frozen_balance=user.frozen_balance,
        deposit_form=deposit_form, withdraw_form=withdraw_form
    )
