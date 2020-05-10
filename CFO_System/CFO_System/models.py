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
class Shop(db.Model):
    __tablename__ = 'shops'
    shop_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    shop_name = db.Column(db.String(32),index=True)
    # shop_avatar = db.Column(db.LargeBinary, default=None)
    shop_info = db.Column(db.String(256))
    shop_delivery_fee = db.Column(db.Integer, default=0)
    shop_rate_total = db.Column(db.Integer)
    shop_rate_number = db.Column(db.Integer)
    shop_balance = db.Column(db.Float)
    shop_contact = db.Column(db.String(11))
    shop_location = db.Column(db.String(32))
    shop_location_detail = db.Column(db.Text(256))
    shop_license_number = db.Column(db.String(32))
    shop_status = db.Column(db.Enum('open', 'closed', 'blocked', 'cancelled'), nullable=False)

    # relationship: shop and product
    products = db.relationship('Product', back_populates='shop', cascade='all, delete-orphan')
    user = db.relationship('User', back_populates='shops') # user and shops
    orders = db.relationship('Order', back_populates='shop', cascade='all, delete-orphan') # shop and orders
    bookmarked_by_users = db.relationship('User', secondary='bookmarks', back_populates='bookmarked_shops') # shops and users whom they bookmarked by

    def get_id(self):
       try:
           return str(self.shop_id)
       except AttributeError:
           raise NotImplementedError("No 'id' attribute - override get_id")


# product database model
class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id'))
    product_name = db.Column(db.String(32),index=True)
    # product_avatar = db.Column(db.LargeBinary)
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
    __tablename__ = 'administrators'
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
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True,nullable=False,index=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    user_password = db.Column(db.String(64), nullable=False)
    user_name = db.Column(db.String(32), nullable=False, index=True)
    # user_avatar = db.Column(db.LargeBinary, default=None)
    user_contact = db.Column(db.String(32), default='')
    available_balance = db.Column(db.Float, default=0)
    frozen_balance = db.Column(db.Float, default=0)
    user_status = db.Column(db.Enum('normal', 'blocked'), nullable=False, default='normal')

    # relationships
    shops = db.relationship('Shop', back_populates='user', cascade='all, delete-orphan') # user and shops
    orders = db.relationship('Order', back_populates='user', cascade='all, delete-orphan') # user and orders
    applications = db.relationship('Application', back_populates='user', cascade='all, delete-orphan') # user and applications
    bookmarked_shops = db.relationship('Shop', secondary='bookmarks', back_populates='bookmarked_by_users') # users and shops which they bookmarked

    def set_password(self, password):
        self.user_password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.user_password, password)

    def get_id(self):
       try:
           return str(self.user_id)
       except AttributeError:
           raise NotImplementedError("No 'id' attribute - override get_id")



class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True,autoincrement=True, nullable=False, unique=True, index=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    user_contact = db.Column(db.String(32), nullable=False)
    user_location = db.Column(db.String(32))
    delivery_fee = db.Column(db.Integer, nullable=False, default=0)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    order_status = db.Column(db.Enum('pending', 'approved', 'denied', 'delivering', 'finished', 'cancelled'), nullable=False)

    # relationships
    user = db.relationship('User', back_populates='orders') # user and orders
    shop = db.relationship('Shop', back_populates='orders') # shop and orders
    purchased_products = db.relationship('Purchased_Product', back_populates='order', cascade='all, delete-orphan') # order and purchased products


class Purchased_Product(db.Model):
    __tablename__ = 'purchased_products'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, index=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), primary_key=True, nullable=False, index=True)
    product_name = db.Column(db.String(32), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # relationships
    order = db.relationship('Order', back_populates='purchased_products') # order and purchased products


class Application(db.Model):
    __tablename__ = 'applications'
    application_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    application_type = db.Column(db.Enum('open', 'cancel','unblock'), nullable=False)
    shop_id = db.Column(db.Integer)
    shop_name = db.Column(db.String(32))
    shop_info = db.Column(db.String(256),  default='')
    shop_contact = db.Column(db.String(32))
    shop_location = db.Column(db.String(32))
    shop_location_detail = db.Column(db.String(256), default='')
    shop_license_number = db.Column(db.String(32), nullable=False)
    application_status = db.Column(db.Enum('pending', 'approved', 'denied'), nullable=False)

    # relationships
    user = db.relationship('User', back_populates='applications') # user and applications


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True, nullable=False, index=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id'), primary_key=True, nullable=False, index=True)
