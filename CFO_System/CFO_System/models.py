# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""

from datetime import datetime

from CFO_System.extensions import db

# shop database model is designed according to the proposal.
# TODO: deleted time, user_id not used yet
class Shop(db.Model):
   #  __tablename__ = 'Shop'
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    shop_name = db.Column(db.String(32),index=True)
    # shop_avatar = db.Column(db.LargeBinary)
    shop_info = db.Column(db.String(256))
    shop_delivery_fee = db.Column(db.Integer, default=0)
    shop_rate = db.Column(db.Integer)
    shop_rate_number = db.Column(db.Integer)
    shop_balance = db.Column(db.Float)
    shop_contact = db.Column(db.String(11))
    shop_location = db.Column(db.Enum(
        'Student Center', 'Shaw College', 'Muse College', 'Deligentia College', 'Harmonia College',
        'Le Tian Building', 'Zhi Ren Building', 'Zhi Xin Building', 'Research A', 'Research B',
        'Teaching A', 'Teaching B', 'Teaching C', 'Teaching D'), nullable=False)
    shop_location_detail = db.Column(db.Text(256))
    shop_license_number = db.Column(db.String(32))
    shop_status = db.Column(db.Enum('open', 'closed', 'blocked', 'cancelled'), nullable=False)

    # relationship: shop and product
    products = db.relationship('Product', back_populates='shop')
    # user = db.relationship('User', back_populates='shops') # user and shops

# product database model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    product_name = db.Column(db.String(32),index=True)
    # product_avatar =
    product_info = db.Column(db.Text(256))
    product_price = db.Column(db.Float)
    total_sale = db.Column(db.Integer)
    # relationship: shop and product
    shop = db.relationship('Shop',back_populates='products')

# administrator database model
class Administrator(db.Model):
    # __tablename__ = 'Administrator'
    administrator_name = db.Column(db.String(32), primary_key=True, nullable=False, unique=True, index=True)
    administrator_password = db.Column(db.String(64), nullable=False)

# user database model
# class User(db.Model):
#     # __tablename__ = 'User'
#     user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
#     email = db.Column(db.String(64), nullable=False, unique=True)
#     user_password = db.Column(db.String(64), nullable=False)
#     user_name = db.Column(db.String(32), nullable=False, default='Unnamed User')
#     user_avatar = db.Column(db.LargeBinary, default=None)
#     user_contact = db.Column(db.String(32), nullable=False, default='')
#     available_balance = db.Column(db.Float, nullable=False)
#     frozen_balance = db.Column(db.Float, nullable=False)
#     user_status = db.Column(db.Enum('normal', 'blocked'), nullable=False, default='normal')
#
#     # relationships
#     shops = db.relationship('Shop', back_populates='user', cascade='all, delete-orphan') # user and shops
#     # orders = db.relationship('orders', back_populates='user', cascade='all, delete-orphan') # user and orders
#     # applications = db.relationship('applications', back_populates='user', cascade='all, delete-orphan') # user and applications
#


