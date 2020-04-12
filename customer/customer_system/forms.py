# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange


class LoginForm(FlaskForm):
    email = StringField('E-mail Address', validators=[DataRequired(), Email(), Length(1, 64)])
    user_password = PasswordField('Password', validators=[DataRequired(), Length(8, 64)])
    submit = SubmitField(label='Login')


class LogoutForm(FlaskForm):
    submit_logout = SubmitField(label='Logout')


class RegisterForm(FlaskForm):
    email = StringField('Enter Your E-mail Address', validators=[DataRequired(), Email(), Length(1, 64)])
    user_password = PasswordField('Set Your Password', validators=[DataRequired(), Length(8, 64)])
    submit = SubmitField(label='Register')


class PasswordForm(FlaskForm):
    user_password = PasswordField('Password', validators=[DataRequired(), Length(8, 64)])
    submit_password = SubmitField(label='Change Password')


class NameForm(FlaskForm):
    user_name = StringField('Name', validators=[DataRequired(), Length(1, 32)])
    submit_name = SubmitField(label='Change Name')


class ContactForm(FlaskForm):
    user_contact = StringField('Contact', validators=[Length(0, 32)])
    submit_contact = SubmitField(label='Change Contact')


class DepositForm(FlaskForm):
    deposit_amount = FloatField('Deposit Amount', validators=[DataRequired(), NumberRange(min=0, max=1000)])
    bank_card_deposit = StringField('Bank Card Number', validators=[DataRequired(), Length(16, 19)])
    submit_deposit = SubmitField(label='Deposit')


class WithdrawForm(FlaskForm):
    withdraw_amount = FloatField('Withdraw Amount', validators=[DataRequired(), NumberRange(min=0, max=1000)])
    bank_card_withdraw = StringField('Bank Card Number', validators=[DataRequired(), Length(16, 19)])
    submit_withdraw = SubmitField(label='Withdraw')
