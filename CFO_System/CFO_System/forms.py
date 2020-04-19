# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField, FloatField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, NumberRange, EqualTo, Regexp, Email
from wtforms import ValidationError


from CFO_System.models import User

# shop info form is designed according to web page v2.2 p.16
class ShopInfoForm(FlaskForm):
    status = [('open','open'), ('closed','closed')]
    location = [('Student Center','Student Center'), ('Shaw College','Shaw College'),
            ('Muse College','Muse College'), ('Deligentia College','Deligentia College'),
            ('Harmonia College','Harmonia College'),('Le Tian Building','Le Tian Building'),
            ('Zhi Ren Building','Zhi Ren Building'), ('Zhi Xin Building','Zhi Xin Building'),
            ('Research A','Research A'), ('Research B','Research B'),('Teaching A','Teaching A'),
            ('Teaching B','Teaching B'), ('Teaching C','Teaching C'), ('Teaching D','Teaching D')]
    shop_name = StringField('店铺名', validators=[DataRequired(), Length(1, 32)])
    shop_contact = StringField('电话', validators=[DataRequired(), Length(11,11)])
    shop_location = SelectField('地点', choices=location,validators=[DataRequired()])
    shop_location_detail = TextAreaField('详细地址', validators=[DataRequired(), Length(1, 256)])
    shop_license_number = StringField('证件号', validators=[DataRequired(), Length(32)])
    shop_info = TextAreaField('详细信息', validators=[DataRequired(), Length(1, 256)])
    shop_delivery_fee = RadioField('运费', choices=[('0',0),('1',1),('2',2),('3',3),('4',4),('5',5)], validators=[DataRequired()])
    shop_status = SelectField('店铺状态',choices=status,validators=[DataRequired()])

    submit = SubmitField('确认修改')

class ShopAddingForm(FlaskForm):
    status = [('open','open'), ('closed','closed'), ('blocked','blocked'), ('cancelled','cancelled')]
    location = [('Student Center','Student Center'), ('Shaw College','Shaw College'),
            ('Muse College','Muse College'), ('Deligentia College','Deligentia College'),
            ('Harmonia College','Harmonia College'),('Le Tian Building','Le Tian Building'),
            ('Zhi Ren Building','Zhi Ren Building'), ('Zhi Xin Building','Zhi Xin Building'),
            ('Research A','Research A'), ('Research B','Research B'),('Teaching A','Teaching A'),
            ('Teaching B','Teaching B'), ('Teaching C','Teaching C'), ('Teaching D','Teaching D')]
    shop_name = StringField('店铺名', validators=[DataRequired(), Length(1, 32)])
    shop_contact = StringField('电话', validators=[DataRequired(), Length(11,11)])
    shop_location = SelectField('地点', choices=location,validators=[DataRequired()])
    shop_location_detail = TextAreaField('详细地址', validators=[DataRequired(), Length(1, 256)])
    shop_license_number = StringField('证件号', validators=[DataRequired(), Length(32)])
    shop_info = TextAreaField('详细信息', validators=[DataRequired(), Length(1, 256)])

    submit = SubmitField('确认提交申请')

# product info form
class ProductInfoForm(FlaskForm):
    product_name = StringField('菜品名', validators=[DataRequired(), Length(1, 32)])
    product_price = FloatField('价格', validators=[DataRequired(), NumberRange(min=0)])
    product_info = TextAreaField('菜品信息', validators=[DataRequired(), Length(1, 256)])
    submit = SubmitField('确认修改')

# submit form for deletion
class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')

# login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    submit = SubmitField('Log in')

# register form
class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 254), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 20),
                                                   Regexp('^[a-zA-Z0-9]*$',
                                                          message='The username should contain only a-z, A-Z and 0-9.')])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField()

    def validate_username(self, field):
        if User.query.filter_by(user_name=field.data).first():
            raise ValidationError('The username is already in use.')

'''
From PasswordForm to WithdrawForm:
Forms for user personal centers
'''

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

class BlockButtonForm(FlaskForm):
    submit_one = SubmitField(label="block this shop")

class ApproveButtonForm(FlaskForm):
    submit_approve = SubmitField(label="Approve")

class RejectButtonForm(FlaskForm):
    submit_reject = SubmitField(label="Reject")
