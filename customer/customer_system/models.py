# -*- coding: utf-8 -*-
'''
All attributes except avatar must not be null.

All valid values for shops.shop_location and applications.shop_location are
'Student Center', 'Shaw College', 'Muse College', 'Deligentia College', 'Harmonia College',
'Le Tian Building', 'Zhi Ren Building', 'Zhi Xin Building', 'Research A', 'Research B',
'Teaching A', 'Teaching B', 'Teaching C', 'Teaching D'.

All valid values for orders.user_location are
'Student Center', 'Shaw College', 'Muse College', 'Deligentia College', 'Harmonia College',
'Le Tian Building', 'Zhi Ren Building', 'Zhi Xin Building', 'Cheng Dao Building', 'Dao Yuan Building',
'Li Wen Building', 'Qi Xian Building', 'Sports Hall', 'Administration Building',
'Research A', 'Research B', 'Teaching A', 'Teaching B', 'Teaching C', 'Teaching D',
'Staff Residence 1', 'Staff Residence 2', 'Staff Residence 3', 'Staff Residence 4'.
'''

from datetime import datetime

from customer_system import db


class Administrator(db.Model):
    __tablename__ = 'administrators'
    administrator_name = db.Column(db.String(32), primary_key=True, nullable=False, unique=True, index=True)
    administrator_password = db.Column(db.String(64))


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    user_password = db.Column(db.String(64))
    user_name = db.Column(db.String(32))
    user_avatar = db.Column(db.LargeBinary)
    user_contact = db.Column(db.String(32))
    available_balance = db.Column(db.Float)
    frozen_balance = db.Column(db.Float)
    user_status = db.Column(db.Enum('normal', 'blocked'))

    shops = db.relationship('Shop', back_populates='user', cascade='all, delete-orphan') # user and shops
    orders = db.relationship('Order', back_populates='user', cascade='all, delete-orphan') # user and orders
    applications = db.relationship('Application', back_populates='user', cascade='all, delete-orphan') # user and applications
    bookmarked_shops = db.relationship('Shop', secondary='bookmarks', back_populates='bookmarked_by_users') # users and shops which they bookmarked


class Shop(db.Model):
    __tablename__ = 'shops'
    shop_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    shop_name = db.Column(db.String(32), index=True)
    shop_avatar = db.Column(db.LargeBinary)
    shop_info = db.Column(db.String(256))
    shop_delivery_fee = db.Column(db.Integer)
    shop_rate_total = db.Column(db.Integer)
    shop_rate_number = db.Column(db.Integer)
    shop_balance = db.Column(db.Float)
    shop_contact = db.Column(db.String(32))
    shop_location = db.Column(db.String(32))
    shop_location_detail = db.Column(db.String(256))
    shop_license_number = db.Column(db.String(32))
    shop_status = db.Column(db.Enum('open', 'closed', 'blocked', 'cancelled'))

    user = db.relationship('User', back_populates='shops') # user and shops
    products = db.relationship('Product', back_populates='shop', cascade='all, delete-orphan') # shop and products
    orders = db.relationship('Order', back_populates='shop', cascade='all, delete-orphan') # shop and orders
    bookmarked_by_users = db.relationship('User', secondary='bookmarks', back_populates='bookmarked_shops') # shops and users whom they bookmarked by


class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id'), nullable=False, index=True)
    product_name = db.Column(db.String(32), index=True)
    product_avatar = db.Column(db.LargeBinary)
    product_info = db.Column(db.String(256))
    product_price = db.Column(db.Float)
    total_sale = db.Column(db.Integer)

    shop = db.relationship('Shop', back_populates='products') # shop and products


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    user_location = db.Column(db.String(32))
    phone_number = db.Column(db.String(32))
    delivery_fee = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    order_status = db.Column(db.Enum('pending', 'approved', 'denied', 'delivering', 'finished', 'cancelled'))

    user = db.relationship('User', back_populates='orders') # user and orders
    shop = db.relationship('Shop', back_populates='orders') # shop and orders
    purchased_products = db.relationship('Purchased_Product', back_populates='order', cascade='all, delete-orphan') # order and purchased products


class Purchased_Product(db.Model):
    __tablename__ = 'purchased_products'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False, index=True)
    product_name = db.Column(db.String(32))
    product_price = db.Column(db.Float)
    quantity = db.Column(db.Integer)

    order = db.relationship('Order', back_populates='purchased_products') # order and purchased products


class Application(db.Model):
    __tablename__ = 'applications'
    application_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    application_type = db.Column(db.Enum('open', 'cancel'))
    shop_name = db.Column(db.String(32))
    shop_info = db.Column(db.String(256))
    shop_contact = db.Column(db.String(32))
    shop_location = db.Column(db.String(32))
    shop_location_detail = db.Column(db.String(256))
    shop_license_number = db.Column(db.String(32))
    application_status = db.Column(db.Enum('pending', 'approved', 'denied'))

    user = db.relationship('User', back_populates='applications') # user and applications


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True, nullable=False, index=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id'), primary_key=True, nullable=False, index=True)
