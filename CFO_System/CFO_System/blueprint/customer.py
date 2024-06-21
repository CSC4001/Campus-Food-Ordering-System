from flask import flash, redirect, url_for, render_template, abort, Blueprint
from flask_login import  login_required, current_user
from CFO_System.models import *
from CFO_System.forms import *

customer_bp = Blueprint("customer", __name__)

'''
index route "/" : display the index of the website
'''
@customer_bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('customer/index.html')

@customer_bp.route('/personal_center', methods=['GET', 'POST'])
@login_required
def personal_center():
    user = User.query.get(current_user.user_id)
    password_form = PasswordForm()
    name_form = NameForm()
    contact_form = ContactForm()
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()

    if password_form.submit_password.data and password_form.validate_on_submit():
        user.set_password(password_form.user_password.data)
        db.session.commit()
        flash('You have successfully changed your password!')
        return redirect(url_for('customer.personal_center'))

    if name_form.submit_name.data and name_form.validate_on_submit():
        user.user_name = name_form.user_name.data
        db.session.commit()
        flash('You have successfully changed your name!')
        return redirect(url_for('customer.personal_center'))

    if contact_form.submit_contact.data and contact_form.validate_on_submit():
        user.user_contact = contact_form.user_contact.data
        db.session.commit()
        flash('You have successfully changed your contact!')
        return redirect(url_for('customer.personal_center'))

    if deposit_form.submit_deposit.data and deposit_form.validate_on_submit():
        amount = round(deposit_form.deposit_amount.data, 2)
        if user.available_balance + amount <= 10000:
            user.available_balance = round(user.available_balance + amount, 2)
            db.session.commit()
            flash('You have successfully deposited {}!'.format(amount))
        else:
            flash('Exceed maximum balance limit!')
        return redirect(url_for('customer.personal_center'))

    if withdraw_form.submit_withdraw.data and withdraw_form.validate_on_submit():
        amount = round(withdraw_form.withdraw_amount.data, 2)
        if user.available_balance - amount >= 0:
            user.available_balance = round(user.available_balance - amount, 2)
            db.session.commit()
            flash('You have successfully withdrew {}!'.format(amount))
        else:
            flash('Insufficient funds!')
        return redirect(url_for('customer.personal_center'))

    name_form.user_name.data = user.user_name
    contact_form.user_contact.data = user.user_contact
    return render_template('customer/personal_center.html', user_id=user.user_id, email=user.email,
        password_form=password_form, name_form=name_form, contact_form=contact_form,
        available_balance=user.available_balance, frozen_balance=user.frozen_balance,
        deposit_form=deposit_form, withdraw_form=withdraw_form
    )
