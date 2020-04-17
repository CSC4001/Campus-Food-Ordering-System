# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""

from datetime import datetime

from CFO_System.extensions import db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


# shop database model is designed according to the proposal.
# TODO: deleted time, user_id not used yet
class Shop(db.Model):
   #  __tablename__ = 'Shop'
    shop_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False, index=True)
    shop_name = db.Column(db.String(32),index=True)
    # shop_avatar = db.Column(db.LargeBinary)
    shop_info = db.Column(db.String(256))
    shop_delivery_fee = db.Column(db.Integer, default=0)
    shop_rate = db.Column(db.Integer)
    shop_rate_number = db.Column(db.Integer)
    shop_balance = db.Column(db.Float)
    shop_contact = db.Column(db.String(32))
    shop_location = db.Column(db.Enum(
        'Student Center', 'Shaw College', 'Muse College', 'Deligentia College', 'Harmonia College',
        'Le Tian Building', 'Zhi Ren Building', 'Zhi Xin Building', 'Research A', 'Research B',
        'Teaching A', 'Teaching B', 'Teaching C', 'Teaching D'), nullable=False)
    shop_location_detail = db.Column(db.Text(256))
    shop_license_number = db.Column(db.String(32))
    shop_status = db.Column(db.Enum('open', 'closed', 'blocked', 'cancelled'), nullable=False)
    # relationship: shop and product
    products = db.relationship('Product', back_populates='shop')
    user = db.relationship('User', back_populates='shops') # user and shops

    def get_id(self):
       try:
           return str(self.shop_id)
       except AttributeError:
           raise NotImplementedError("No 'id' attribute - override get_id")



# product database model
class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.shop_id'))
    product_name = db.Column(db.String(32),index=True)
    # product_avatar =
    product_info = db.Column(db.Text(256))
    product_price = db.Column(db.Float)
    total_sale = db.Column(db.Integer)
    # relationship: shop and product
    shop = db.relationship('Shop',back_populates='products')

    def get_id(self):
       try:
           return str(self.product_id)
       except AttributeError:
           raise NotImplementedError("No 'id' attribute - override get_id")

# administrator databse model, different from regular users
class Administrator(db.Model, UserMixin):
    # __tablename__ = 'Administrator'
    admin_id = db.Column(db.Integer, primary_key=True)
    administrator_name = db.Column(db.String(32), unique=True, index=True)
    administrator_password = db.Column(db.String(128))

    def set_password(self, password):
        self.administrator_password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.administrator_password, password)

    def get_id(self):
       try:
           return str(self.admin_id)
       except AttributeError:
           raise NotImplementedError("No 'id' attribute - override get_id")

# user database model
class User(db.Model, UserMixin):
    # __tablename__ = 'User'
    user_id = db.Column(db.Integer, primary_key=True,nullable=False,index=True)
    email = db.Column(db.String(64), nullable=False)
    user_password = db.Column(db.String(64), nullable=False)
    user_name = db.Column(db.String(32), nullable=False, unique=True, index=True)
    user_avatar = db.Column(db.LargeBinary, default=None)
    user_contact = db.Column(db.String(32), default='')
    available_balance = db.Column(db.Float, default=0)
    frozen_balance = db.Column(db.Float, default=0)
    user_status = db.Column(db.Enum('normal', 'blocked'), nullable=False, default='normal')
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))

    # relationships
    role = db.relationship('Role',back_populates='users')
    shops = db.relationship('Shop', back_populates='user', cascade='all, delete-orphan') # user and shops
    # orders = db.relationship('orders', back_populates='user', cascade='all, delete-orphan') # user and orders
    # applications = db.relationship('applications', back_populates='user', cascade='all, delete-orphan') # user and applications

    def set_password(self, password):
        self.user_password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.user_password, password)

    def get_id(self):
       try:
           return str(self.user_id)
       except AttributeError:
           raise NotImplementedError("No 'id' attribute - override get_id")


'''
Role and permission models
'''

# relationship table
roles_permissions = db.Table('roles_permissions',
                             db.Column('role_id', db.Integer, db.ForeignKey('role.role_id')),
                             db.Column('permission_id', db.Integer, db.ForeignKey('permission.permission_id'))
                             )

class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(30), unique=True)
    users = db.relationship('User',back_populates='role')
    permissions = db.relationship('Permission',secondary=roles_permissions, back_populates='roles')


class Permission(db.Model):
    permission_id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(30), unique=True)
    roles = db.relationship('Role',secondary=roles_permissions, back_populates='permissions')




