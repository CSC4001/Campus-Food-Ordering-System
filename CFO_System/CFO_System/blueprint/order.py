# -*- coding: utf-8 -*-

from flask import flash, redirect, url_for, render_template, abort, Blueprint, request,jsonify
from flask_login import login_required, current_user
from CFO_System.models import *
from CFO_System.utils import *
from CFO_System.blueprint.shop import shop_bp
from CFO_System.blueprint.auth import auth_bp
from CFO_System.blueprint.customer import customer_bp
from CFO_System.blueprint.admin import admin_bp
from datetime import datetime

'''
Return all order informations
request:
data = {
    "method":"GET"(GET/POST)
}
response:
data = {
    list: [
        {
            "order_id":
            "shop_id":
            ...
        }
        {
        ...
    ]
}
'''
@admin_bp.route('/order_management',methods=['GET','POST'])
@login_required
def order_management():
    response_object = {"list":list()}
    if request.method == 'GET':
        request_object = request.get_json()
        if request_object is None:
            return jsonify(message=('Invalid item body.')), 400
        orders = Order.query.order_by(Order.create_time.desc()).all()
        if orders == None:
            return jsonify(message=("Orders empty.")), 400
        for order in orders:
            info = {
                "order_id":order.order_id,
                "shop_id" : order.shop_id,
                "shop_name" : Shop.query.filter_by(shop_id=order.shop_id).first().shop_name,
                "user_id" : order.user_id,
                "user_location" : order.user_location,
                "delivery_fee" : order.delivery_fee,
                "create_time": order.create_time,
                "order_status": order.order_status
            }
            response_object['list'].append(info)
        return jsonify(data=response_object)

'''
Return detail order info of one order
request:
data = {
    "method":"GET"(GET/POST),
    "order_id":1
}
response:
data = {
    list: [
        {
            "order_id":
            "product_id":
            ...
        }
        {
        ...
    ]
}
'''
@admin_bp.route('/order_detail',methods=['GET','POST'])
@login_required
def order_detail():
    response_object = {"list":list()}
    if request.method == 'GET':
        request_object = request.get_json()
        if request_object is None:
            return jsonify(message=('Invalid item body.')), 400
        order_id = request_object.get("order_id")
        if order_id == None:
            return jsonify(message=('Invalid item body.')), 400
        products = Purchased_Product.query.filter_by(order_id=order_id).all()
        if products == None:
            return jsonify(message=("Request id do not exist.")), 404
        for product in products:
            info = dict()
            info["product_id"] = product.product_id
            info["order_id"] = order_id
            info["product_name"] = product.product_name
            info["product_price"] = product.product_price
            info["quantity"] = product.quantity
            response_object['list'].append(info)
        return jsonify(data=response_object)

'''
Customer: check all orders
request:
data = {
    "method":"GET"(GET/POST),
    "user_id": 1
}
response:
data = {
    list: [
        {
            "order_id":
            "product_id":
            ...
        }
        {
        ...
    ]
}
'''
@customer_bp.route('/my_orders',methods=['GET','POST'])
@login_required
def my_orders():
    response_object = {"list":list()}
    if request.method == 'GET':
        request_object = request.get_json()
        if request_object is None:
            return jsonify(message=('Invalid item body.')), 400
        user_id = request_object.get("user_id")
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.create_time.desc()).all()
        if orders == None:
            return jsonify(message=("Orders empty.")), 400
        for order in orders:
            info = {
                "order_id":order.order_id,
                "shop_name" : Shop.query.filter_by(shop_id=order.shop_id).first().shop_name,
                "user_contact": order.user_contact,
                "user_location" : order.user_location,
                "delivery_fee" : order.delivery_fee,
                "create_time": order.create_time,
                "order_status": order.order_status
            }
            response_object['list'].append(info)
        return jsonify(data=response_object)

'''
Customer: Return detail order info of one order
request:
data = {
    "method":"GET"(GET/POST),
    "order_id":1
}
response:
data = {
    list: [
        {
            "order_id":
            "product_id":
            ...
        }
        {
        ...
    ]
}
'''
@customer_bp.route('/order_detail',methods=['GET','POST'])
@login_required
def my_order_detail():
    response_object = {"list":list()}
    if request.method == 'GET':
        request_object = request.get_json()
        if request_object is None:
            return jsonify(message=('Invalid item body.')), 400
        order_id = request_object.get("order_id")
        if order_id == None:
            return jsonify(message=('Invalid item body.')), 400
        products = Purchased_Product.query.filter_by(order_id=order_id).all()
        if products == None:
            return jsonify(message=("Request id do not exist.")), 404
        for product in products:
            info = dict()
            info["product_name"] = product.product_name
            info["product_price"] = product.product_price
            info["quantity"] = product.quantity
            response_object['list'].append(info)
        return jsonify(data=response_object)

'''
Shop: check all orders
request:
data = {
    "method":"GET"(GET/POST)
    "shop_id": 1
}
response:
data = {
    list: [
        {
            "order_id":
            "shop_id":
            ...
        }
        {
        ...
    ]
}
'''
@shop_bp.route('/order_management',methods=['GET','POST'])
@login_required
def shop_orders():
    response_object = {"list":list()}
    if request.method == 'GET':
        request_object = request.get_json()
        if request_object is None:
            return jsonify(message=('Invalid item body.')), 400
        shop_id = request_object.get("shop_id")
        orders = Order.query.filter_by(shop_id=shop_id).order_by(Order.create_time.desc()).all()
        if orders == None:
            return jsonify(message=("Orders empty.")), 400
        for order in orders:
            info = {
                "order_id":order.order_id,
                "shop_name" : Shop.query.filter_by(shop_id=order.shop_id).first().shop_name,
                "user_id" : order.user_id,
                "user_location" : order.user_location,
                "user_contact": order.user_contact,
                "delivery_fee" : order.delivery_fee,
                "create_time": order.create_time,
                "order_status": order.order_status
            }
            response_object['list'].append(info)
        return jsonify(data=response_object)

'''
Shop: Return detail order info of one order
request:
data = {
    "method":"GET"(GET/POST),
    "order_id":1
}
response:
data = {
    list: [
        {
            "order_id":
            "product_id":
            ...
        }
        {
        ...
    ]
}
'''
@shop_bp.route('/order_detail',methods=['GET','POST'])
@login_required
def shop_order_detail():
    response_object = {"list":list()}
    if request.method == 'GET':
        request_object = request.get_json()
        if request_object is None:
            return jsonify(message=('Invalid item body.')), 400
        order_id = request_object.get("order_id")
        if order_id == None:
            return jsonify(message=('Invalid item body.')), 400
        products = Purchased_Product.query.filter_by(order_id=order_id).all()
        if products == None:
            return jsonify(message=("Request id do not exist.")), 404
        for product in products:
            info = dict()
            info["product_name"] = product.product_name
            info["product_price"] = product.product_price
            info["quantity"] = product.quantity
            response_object['list'].append(info)
        return jsonify(data=response_object)

'''
Customer: pay and create an order
request:
data = {
    "method":"POST"(GET/POST),
    "form":{
        "shop_id":
        "user_id":
        "user_contact":
        "user_location":
        
    }
    "list":[
        {
            "product_id":
            "quantity":
        }
    ]
    
}
response:
data = {
    "message":
}
'''
@customer_bp.route('/create_order',methods=['POST'])
@login_required
def create_order():
    response_object = dict()
    request_object = request.get_json()
    if request_object is None:
        return jsonify(message=('Invalid item body.')), 400
    request_form = request_object.get("form")
    request_list = request_object.get("list")
    # create order
    delivery_fee = Shop.query.filter_by(shop_id=request_form.get("shop_id")).first().shop_delivery_fee
    order = Order(
        shop_id = request_form.get("shop_id"),
        user_id = request_form.get("user_id"),
        user_contact = request_form.get("user_contact"),
        user_location = request_form.get("user_location"),
        delivery_fee = delivery_fee,
        create_time = datetime.utcnow(),
        order_status = "pending"
    )
    db.session.add(order)
    # add products to the order
    price = 0
    for info in request_list:
        product_id = info.get("product_id")
        quantity = info.get("quantity")
        product_price = Product.query.filter_by(product_id=product_id).first().product_price
        product = Purchased_Product(
            product_id = product_id,
            product_name = Product.query.filter_by(product_id=product_id).first().product_name,
            product_price = product_price,
            quantity = quantity
        )
        price += product_price
        db.session.add(product)
        order.purchased_products.append(product)
    # freeze some balance when creating order
    user = User.query.filter_by(user_id=request_form.get("user_id")).first()
    balance_amount = delivery_fee + price
    user.available_balance -= balance_amount
    user.frozen_balance += balance_amount
    db.session.commit()
    response_object["message"] = "Successfully create order!"
    return jsonify(data=response_object)

'''
Customer: cancel order when it is still pending
request:
data = {
    "method":"POST"(GET/POST),
    "form":{
        "order_id":
    }
    
}
response:
data = {
    "message":
}
'''
@customer_bp.route('/cancel_order',methods=['POST'])
@login_required
def cancel_order():
    response_object = dict()
    request_object = request.get_json()
    if request_object is None:
        return jsonify(message=('Invalid item body.')), 400
    request_form = request_object.get("form")
    order_id = request_form.get("order_id")
    order = Order.query.filter_by(order_id=order_id).first()
    order.order_status = "cancelled"
    db.session.commit()
    response_object["message"] = "Successfully cancel order!"
    return jsonify(data=response_object)

'''
Customer: pay the order
request:
data = {
    "method":"POST"(GET/POST),
    "form":{
        "order_id":
    }
    
}
response:
data = {
    "message":
}
'''
@customer_bp.route('/pay_order',methods=['POST'])
@login_required
def pay_order():
    response_object = dict()
    request_object = request.get_json()
    if request_object is None:
        return jsonify(message=('Invalid item body.')), 400
    request_form = request_object.get("form")
    order_id = request_form.get("order_id")
    order = Order.query.filter_by(order_id=order_id).first()
    if order.order_status != 'approved' or order.order_status != 'delivering':
        return jsonify(message=('Invalid order status.')), 400
    order.order_status = "finished"
    # transaction of balance
    user_id = order.user_id
    user = User.query.filter_by(user_id=user_id).first()
    shop = Shop.query.filter_by(shop_id=order.shop_id).first()
    balance_amount = user.frozen_balance
    user.frozen_balance=0
    shop.shop_balance += balance_amount
    db.session.commit()
    response_object["message"] = "Successfully pay order!"
    return jsonify(data=response_object)

'''
Customer: rating a shop after one order is finished
request:
data = {
    "method":"POST"(GET/POST),
    "form":{
        "shop_id":
        "rate":
    }
    
}
response:
data = {
    "message":
}
'''
@customer_bp.route('/rate_order',methods=['POST'])
@login_required
def rate_order():
    response_object = dict()
    request_object = request.get_json()
    if request_object is None:
        return jsonify(message=('Invalid item body.')), 400
    request_form = request_object.get("form")
    shop = Shop.query.filter_by(shop_id=request_form.get('shop_id')).first()
    shop.shop_rate_total += request_form.get("rate")
    shop.shop_rate_number += 1
    db.session.commit()
    response_object["message"] = "Successfully updating rate!"
    return jsonify(data=response_object)

'''
Shop: change order status
request:
data = {
    "method":"GET"(GET/POST),
    "form":{
        "order_id":1,
        "status":
    }
    
}
response:
data = {
    "message":
}
'''
@shop_bp.route('/change_order_status',methods=['POST'])
@login_required
def change_order_status():
    response_object = dict()
    request_object = request.get_json()
    if request_object is None:
        return jsonify(message=('Invalid item body.')), 400
    request_form = request_object.get("form")
    order_id = request_form.get("order_id")
    status = request_form.get("status")
    current_status = Order.query.filter_by(order_id=order_id).first().order_status

    if current_status == "finished" or current_status == "cancelled" or current_status == "denied" or current_status == 'delivering':
        return jsonify(message=("Invalid order status. Can't change status now.")), 400
    if current_status == "pending" and (status != "approved" or status != "denied"):
        return jsonify(message=('Invalid order status. Must approve or deny a pending status.')), 400
    if current_status == "approved" and status != 'delivering':
        return jsonify(message=('Invalid order status. Can just change to delivering state.')), 400
    order = Order.query.filter_by(order_id=order_id).first()
    order.order_status = status
    db.session.commit()
    response_object["message"] = "Successfully updating status!"
    return jsonify(data=response_object)

