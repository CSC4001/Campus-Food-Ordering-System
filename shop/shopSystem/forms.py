# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired, Length

# shop info form is designed according to web page v2.2 p.16
class ShopInfoForm(FlaskForm):
    shop_name = StringField('店铺名', validators=[DataRequired(), Length(1, 20)])
    shop_contact = StringField('电话', validators=[DataRequired(), Length(11)])
    shop_location = StringField('地点', validators=[DataRequired(), Length(1, 20)])
    shop_location_detail = TextAreaField('详细地址', validators=[DataRequired(), Length(1, 150)])
    shop_license_number = StringField('证件号', validators=[DataRequired(), Length(9)])
    shop_info = TextAreaField('详细信息', validators=[DataRequired(), Length(1, 200)])
    shop_delivery_fee = RadioField('运费', choices=[('0',0),('1',1),('2',2),('3',3),('4',4),('5',5)], validators=[DataRequired()])

    submit = SubmitField('确认修改')
