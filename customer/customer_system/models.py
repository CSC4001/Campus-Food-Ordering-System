# -*- coding: utf-8 -*-

from datetime import datetime

from customer_system import db


class Administrator(db.Model):
    __tablename__ = 'administrators'
    administrator_name = db.Column(db.String(32), primary_key=True, nullable=False, unique=True, index=True)
    administrator_password = db.Column(db.String(64), nullable=False)


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    user_password = db.Column(db.String(64), nullable=False)
    user_name = db.Column(db.String(32), nullable=False, default='Unnamed User')
    user_avatar = db.Column(db.LargeBinary, default=None)
    user_contact = db.Column(db.String(32), nullable=False, default='')
    available_balance = db.Column(db.Float, nullable=False)
    frozen_balance = db.Column(db.Float, nullable=False)
    user_status = db.Column(db.Enum('normal', 'blocked'), nullable=False, default='normal')

    # relationships
    # shops = db.relationship('shops', back_populates='user', cascade='all, delete-orphan') # user and shops
    # orders = db.relationship('orders', back_populates='user', cascade='all, delete-orphan') # user and orders
    # applications = db.relationship('applications', back_populates='user', cascade='all, delete-orphan') # user and applications


class Shop(db.Model):
    __tablename__ = 'shops'
    shop_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    shop_name = db.Column(db.String(32), nullable=False, index=True)
    shop_avatar = db.Column(db.LargeBinary, default=None)
    shop_info = db.Column(db.String(256), nullable=False, default='')
    shop_delivery_fee = db.Column(db.Integer, nullable=False, default=0)
    shop_rate_total = db.Column(db.Integer, nullable=False)
    shop_rate_number = db.Column(db.Integer, nullable=False)
    shop_balance = db.Column(db.Float, nullable=False)
    shop_contact = db.Column(db.String(32), nullable=False)
    shop_location = db.Column(db.Enum(
        'Student Center', 'Shaw College', 'Muse College', 'Deligentia College', 'Harmonia College',
        'Le Tian Building', 'Zhi Ren Building', 'Zhi Xin Building', 'Research A', 'Research B',
        'Teaching A', 'Teaching B', 'Teaching C', 'Teaching D'), nullable=False)
    shop_location_detail = db.Column(db.String(256), nullable=False, default='')
    shop_license_number = db.Column(db.String(32), nullable=False)
    shop_status = db.Column(db.Enum('open', 'closed', 'blocked', 'cancelled'), nullable=False)

    # relationships
    # user = db.relationship('users', back_populates='shops') # user and shops
    # products = db.relationship('products', back_populates='shop', cascade='all, delete-orphan') # shop and products
    # orders = db.relationship('orders', back_populates='shop', cascade='all, delete-orphan') # shop and orders


class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id'), nullable=False, index=True)
    product_name = db.Column(db.String(32), nullable=False, index=True)
    product_avatar = db.Column(db.LargeBinary, default=None)
    product_info = db.Column(db.String(256), nullable=False, default='')
    product_price = db.Column(db.Float, nullable=False)
    total_sale = db.Column(db.Integer, nullable=False)

    # relationships
    # shop = db.relationship('shops', back_populates='products') # shop and products


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    user_contact = db.Column(db.String(32), nullable=False)
    user_location = db.Column(db.Enum(
        'Student Center', 'Shaw College', 'Muse College', 'Deligentia College', 'Harmonia College', 'Le Tian Building',
        'Zhi Ren Building', 'Zhi Xin Building', 'Cheng Dao Building', 'Dao Yuan Building', 'Li Wen Building', 'Qi Xian Building',
        'Sports Hall', 'Research A', 'Research B', 'Teaching A', 'Teaching B', 'Teaching C', 'Teaching D', 'Administration Building',
        'Staff Residence 1', 'Staff Residence 2', 'Staff Residence 3', 'Staff Residence 4'), nullable=False)
    delivery_fee = db.Column(db.Integer, nullable=False, default=0)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    order_status = db.Column(db.Enum('pending', 'approved', 'denied', 'delivering', 'finished', 'cancelled'), nullable=False)

    # relationships
    # user = db.relationship('users', back_populates='orders') # user and orders
    # shop = db.relationship('shops', back_populates='orders') # shop and orders
    # purchased_products = db.relationship('purchased_products', back_populates='order', cascade='all, delete-orphan') # order and purchased products


class Purchased_Product(db.Model):
    __tablename__ = 'purchased_products'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'), nullable=False, index=True)
    product_name = db.Column(db.String(32), nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    # relationships
    # order = db.relationship('orders', back_populates='purchased_products') # order and purchased products


class Application(db.Model):
    __tablename__ = 'applications'
    application_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, index=True)
    application_type = db.Column(db.Enum('open', 'cancel'), nullable=False)
    shop_name = db.Column(db.String(32), nullable=False)
    shop_info = db.Column(db.String(256), nullable=False, default='')
    shop_contact = db.Column(db.String(32), nullable=False)
    shop_location = db.Column(db.Enum(
        'Student Center', 'Shaw College', 'Muse College', 'Deligentia College', 'Harmonia College',
        'Le Tian Building', 'Zhi Ren Building', 'Zhi Xin Building', 'Research A', 'Research B',
        'Teaching A', 'Teaching B', 'Teaching C', 'Teaching D'), nullable=False)
    shop_location_detail = db.Column(db.String(256), nullable=False, default='')
    shop_license_number = db.Column(db.String(32), nullable=False)
    application_status = db.Column(db.Enum('pending', 'approved', 'denied'), nullable=False)

    # relationships
    # user = db.relationship('users', back_populates='applications') # user and applications


class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True, nullable=False, index=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id'), primary_key=True, nullable=False, index=True)
