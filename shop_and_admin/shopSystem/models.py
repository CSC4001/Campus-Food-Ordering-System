# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""

from datetime import datetime

from shop_and_admin.shopSystem.extensions import db

# shop database model is designed according to the proposal.
# TODO: deleted time, user_id not used yet
class Shop(db.Model):
    shop_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20))
    shop_name = db.Column(db.String(20),index=True)
    # shop_avatar = db.Column(db.LargeBinary)
    shop_info = db.Column(db.String(200))
    shop_delivery_fee = db.Column(db.Integer)
    shop_rate = db.Column(db.Integer)
    shop_rate_number = db.Column(db.Integer)
    shop_balance = db.Column(db.Float)
    shop_contact = db.Column(db.String(11))
    shop_location = db.Column(db.String(20))
    shop_location_detail = db.Column(db.Text(150))
    shop_license_number = db.Column(db.String(9))
    shop_status = db.Column(db.String(20))
    # relationship: shop and product
    products = db.relationship('Product', back_populates='shop')

# product database model
class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.shop_id'))
    product_name = db.Column(db.String(20),index=True)
    # product_avatar =
    product_info = db.Column(db.Text(150))
    product_price = db.Column(db.Float)
    total_sale = db.Column(db.Integer)
    # relationship: shop and product
    shop = db.relationship('Shop',back_populates='products')
