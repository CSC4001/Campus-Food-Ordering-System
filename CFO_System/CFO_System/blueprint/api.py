from flask import render_template, flash, redirect, url_for, Blueprint, request, jsonify, Response
from flask_login import login_user, logout_user, login_required, current_user

from CFO_System.models import *
from CFO_System.forms import *
from CFO_System.utils import redirect_back
from CFO_System.models import User
from CFO_System.extensions import db
import json

api_bp = Blueprint("api",__name__)

# API for auth
# Login
@api_bp.route('/login',methods=['POST'])
def api_login():
    data = request.get_json()
    email = data['email'].lower()
    password = data['password']
    if email == 'admin':
        admin = Administrator.query.filter_by(administrator_name=email).first()
        if email == admin.administrator_name and admin.validate_password(password):
            return jsonify({'status':'admin','info':'登陆成功','session':-1})
    result = User.query.filter_by(email=email).first()
    if result is not None and result.validate_password(password):
        return jsonify({
            'status':'ok',
            'info':'登录成功',
            'session':result.user_id
            })
    return jsonify({
        'status':'no',
        'info':'登录失败'
        })

# Register
@api_bp.route('/register', methods=['GET', 'POST'])
def api_register():
    data = request.get_json()
    email = data['email'].lower()
    username = data['username']
    password = data['password']
    user = User(email=email, user_name=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    test = User.query.filter_by(email=email).first()
    if test.user_name == username:
        return jsonify({'status':'ok','info':'注册成功'})
    return jsonify({'status':'no','info':'注册失败'})

# API for user information
# Pulling user's personal information when page is creating
@api_bp.route('/personalInfo', methods=['GET'])
def api_personalInfo():
    data = request.args.get('id')
    result = User.query.get(data)
    return jsonify({
        'user_id': result.user_id,
        'email': result.email,
        'userName': result.user_name,
        'contact': result.user_contact,
        'available': result.available_balance,
        'frozen': result.frozen_balance,
        'status': result.user_status
    })

# Handle deposit of balance
@api_bp.route('/submitDeposit', methods=['POST'])
def api_submitDeposit():
    data = request.args.get('id')
    amount = request.get_json()['deposit']
    user = User.query.get(data)
    if user.available_balance + amount <= 10000:
        user.available_balance = round(user.available_balance + amount, 2)
        db.session.commit()
        return jsonify({'status':'ok',
        'info':'You have successfully deposit {}!'.format(amount),
        'available': user.available_balance})
    else:
        return jsonify({'status':'no','info':'Insufficient funds!'})

# handle withdraw of balance
@api_bp.route('/submitWithdraw', methods=['POST'])
def api_submitWithdraw():
    data = request.args.get('id')
    amount = request.get_json()['withdraw']
    user = User.query.get(data)
    if user.available_balance - amount >= 0:
        user.available_balance = round(user.available_balance - amount, 2)
        db.session.commit()
        return jsonify({'status':'ok',
        'info':'You have successfully withdraw {}!'.format(amount),
        'available': user.available_balance})
    else:
        return jsonify({'status':'no','info':'Insufficient funds!'})

# handle modification of personal information
@api_bp.route('/submitProsonalInfo', methods=['POST'])
def api_submitProsonalInfo():
    data = request.get_json()
    user = User.query.get(data['user_id'])
    if user.email != data['email']:
        user.email = data['email']
    if user.user_password != data['password'] and data['password']!= '':
        user.set_password(data['password'])
    if user.user_name != data['userName']:
        user.user_name = data['userName']
    if user.user_contact != data['contact']:
        user.user_contact = data['contact']
    try:
        db.session.commit()
        return jsonify({'status':'ok','info':'Modify successfully!'})
    except:
        return jsonify({'status':'no','info':'Modify error!'})

# provide myShop page's shop list
@api_bp.route('/getMyShop', methods=['GET'])
def api_getMyShop():
    data = request.args.get('id')
    messages = Shop.query.filter_by(user_id=data).order_by(Shop.shop_name.desc()).all()
    if len(messages) == 0:
        return jsonify({})
    else:
        result = list()
        for shop in messages:
            a = dict()
            a['shop_id'] = shop.shop_id
            a['shop_name'] = shop.shop_name
            a['shop_info'] = shop.shop_info
            a['shop_status'] = shop.shop_status
            result.append(a)
        return Response(json.dumps(result),  mimetype='application/json')

# submit shop apply form
@api_bp.route('/submitShopApply', methods=['POST'])
def api_submitShopApply():
    data = request.get_json()
    application = Application(
        user_id = data['id'],
        application_type="open",
        shop_name = data['name'],
        shop_contact = data['contact'],
        shop_license_number = data['licenseNum'],
        shop_location = data['location'],
        shop_location_detail = data['locationDetail'],
        shop_info=data['info'],
        application_status="pending"
    )
    db.session.add(application)
    db.session.commit()
    return jsonify({
        'status': 'ok',
        'info': 'Submit success!'
    })

# provide selected shop index
@api_bp.route('/getShopIndex', methods=['GET'])
def api_getShopIndex():
    user_id = request.args.get('user_id')
    shop_id = request.args.get('shop_id')
    shop = Shop.query.filter_by(shop_id=shop_id, user_id=user_id).first_or_404()
    if shop is None:
        return jsonify({
            'status': 'invalid'
        })
    if shop.shop_status == 'cancelled':
        return jsonify({
            'status': 'cancelled'
        })
    return jsonify({
        'status': 'valid',
        'shopid': shop.shop_id,
        'userid': shop.user_id,
        'name': shop.shop_name,
        'info': shop.shop_info,
        'shopStatus': shop.shop_status,
        'rateTotal': shop.shop_rate_total,
        'rateNum': shop.shop_rate_number
    })

# submit cancelling shop apply form
@api_bp.route('/submitCancelApply', methods=['GET'])
def api_submitCancelApply():
    id = request.args.get('id')
    shop = Shop.query.filter_by(shop_id=id).first()
    if shop.shop_status == 'cancelled' or shop.shop_status == 'blocked':
        return jsonify({'status': 'invalid'})
    application = Application(
        user_id=shop.user_id,
        shop_id=shop.shop_id,
        application_type="cancel",
        shop_name = shop.shop_name,
        shop_license_number = shop.shop_license_number,
        application_status="pending"
    )
    db.session.add(application)
    db.session.commit()
    return jsonify({'status': 'success'})

# submit apply for applying unblock the shop
@api_bp.route('/submitUnblockApply', methods=['GET'])
def api_submitUnblockApply():
    id = request.args.get('id')
    shop = Shop.query.filter_by(shop_id=id).first()
    if shop.shop_status != 'blocked':
        return jsonify({'status': 'invalid'})
    application = Application(
        user_id=shop.user_id,
        shop_id=shop.shop_id,
        application_type="unblock",
        shop_name = shop.shop_name,
        shop_license_number = shop.shop_license_number,
        application_status="pending"
    )
    db.session.add(application)
    db.session.commit()
    return jsonify({'status': 'success'})

# provide selected shop information
@api_bp.route('/getShopInfo', methods=['GET'])
def api_getShopInfo():
    user_id = request.args.get('user_id')
    shop_id = request.args.get('shop_id')
    shop = Shop.query.filter_by(shop_id=shop_id, user_id=user_id).first_or_404()
    if shop is None:
        return jsonify({
            'status': 'invalid'
        })
    if shop.shop_status == 'cancelled':
        return jsonify({
            'status': 'cancelled'
        })
    return jsonify({
        'status': 'valid',
        'shopid': shop.shop_id,
        'userid': shop.user_id,
        'contact': shop.shop_contact,
        'name': shop.shop_name,
        'info': shop.shop_info,
        'delivery': shop.shop_delivery_fee,
        'location': shop.shop_location,
        'locationDetail': shop.shop_location_detail,
        'shopStatus': shop.shop_status,
        'licenseNum':shop.shop_license_number,
        'balance': shop.shop_balance
    })

# submit shop info form
@api_bp.route('/submitShopInfo', methods=['POST'])
def api_submitShopInfo():
    data = request.get_json()
    userid = data['userid']
    shopid = data['shopid']
    shop = Shop.query.filter_by(shop_id=shopid, user_id=userid).first_or_404()
    if shop is None:
        return jsonify({
            'status': 'invalid'
        })
    if shop.shop_status == 'blocked':
        return jsonify({
            'status': 'blocked'
        })
    shop.shop_name = data['name']
    shop.shop_contact = data['contact']
    shop.shop_location = data['location']
    shop.shop_location_detail = data['locationDetail']
    shop.shop_license_number = data['licenseNum']
    shop.shop_info = data['info']
    shop.shop_delivery_fee = data['delivery']
    shop.shop_status = data['shopStatus']
    db.session.commit()
    return jsonify({
        'status': 'ok',
        'info': 'Submit success!'
    })


# provide selected shop's dishes information
@api_bp.route('/getDishes', methods=['GET'])
def api_getDishes():
    user_id = request.args.get('user_id')
    shop_id = request.args.get('shop_id')
    shop = Shop.query.filter_by(shop_id=shop_id, user_id=user_id).first_or_404()
    if shop is None:
        return jsonify({
            'status': 'invalid'
        })
    if shop.shop_status == 'blocked':
        return jsonify({
            'status': 'blocked'
        })
    dishes = Product.query.filter_by(shop_id=shop_id).all()
    result = list()
    for i in dishes:
        a = dict()
        a['productid'] = i.product_id
        a['name'] = i.product_name
        a['info'] = i.product_info
        a['price'] = i.product_price
        a['sale'] = i.total_sale
        result.append(a)
    return Response(json.dumps(result),  mimetype='application/json')

# submit dish form
@api_bp.route('/submitDish', methods=['POST'])
def submitDish():
    data = request.get_json()
    userid = data['userid']
    shopid = data['shopid']
    shop = Shop.query.filter_by(shop_id=shopid, user_id=userid).first_or_404()
    if shop is None:
        return jsonify({
            'status': 'invalid'
        })
    product = Product(
        shop_id=shopid,
        product_name=data['name'],
        product_price=data['price'],
        product_info=data['info'],
        total_sale=0
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({
        'status': 'ok'
    })

# edit dish form
@api_bp.route('/editDish', methods=['POST'])
def editDish():
    data = request.get_json()
    userid = data['userid']
    shopid = data['shopid']
    shop = Shop.query.filter_by(shop_id=shopid, user_id=userid).first_or_404()
    if shop is None:
        return jsonify({
            'status': 'invalid'
        })
    product = Product.query.get(data['productid'])
    product.product_name=data['name']
    product.product_price=data['price']
    product.product_info=data['info']
    db.session.commit()
    return jsonify({
        'status': 'ok'
    })

# delete dish
@api_bp.route('/deleteDish', methods=['POST'])
def deleteDish():
    data = request.get_json()
    userid = data['userid']
    shopid = data['shopid']
    productid = data['productid']
    shop = Shop.query.filter_by(shop_id=shopid, user_id=userid).first_or_404()
    if shop is None:
        return jsonify({
            'status': 'invalid'
        })
    product = Product.query.get(productid)
    db.session.delete(product)
    db.session.commit()
    return jsonify({
        'status': 'ok'
    })

# home page get highest rate shops
@api_bp.route('/getRatedShops', methods=['GET'])
def api_getRatedShops():
    shops = Shop.query.order_by(Shop.shop_rate_total.desc()).all()
    result = list()
    i = 0
    for shop in shops:
        if shop.shop_status == 'open':
            i += 1
            a = dict()
            a['shop_id'] = shop.shop_id
            a['shop_name'] = shop.shop_name
            a['shop_info'] = shop.shop_info
            a['shop_rate_total'] = shop.shop_rate_total
            a['shop_rate_number'] = shop.shop_rate_number
            result.append(a)
            if i == 6: break
        else: continue
    return Response(json.dumps(result),  mimetype='application/json')

# home page get highest rate dishes
@api_bp.route('/getRatedDishes', methods=['GET'])
def api_getRatedDishes():
    dishes = Product.query.order_by(Product.total_sale.desc()).all()
    result = list()
    i = 0
    for dish in dishes:
        shop = Shop.query.filter_by(shop_id=dish.shop_id).first()
        if shop.shop_status == 'open':
            i += 1
            a = dict()
            a['product_id'] = dish.product_id
            a['shop_id'] = dish.shop_id
            a['product_name'] = dish.product_name
            a['product_info'] = dish.product_info
            a['total_sale'] = dish.total_sale
            result.append(a)
            if i == 12: break
        else: continue
    return Response(json.dumps(result),  mimetype='application/json')

# get search result by given shop/dish
@api_bp.route('/getSearch', methods=['GET'])
def api_getSearch():
    searchKey = request.args.get('searchKey')
    searchType = request.args.get('searchType')
    if searchType == 'shop':
        shops = Shop.query.filter(Shop.shop_name.like('%' + searchKey + '%')if searchKey is not None else "").all()
        result = list()
        for shop in shops:
            if shop.status == 'open':
                a = dict()
                a['shop_id'] = shop.shop_id
                a['shop_name'] = shop.shop_name
                a['shop_info'] = shop.shop_info
                a['shop_rate_total'] = shop.shop_rate_total
                a['shop_rate_number'] = shop.shop_rate_number
                result.append(a)
            else: continue
        return Response(json.dumps(result),  mimetype='application/json')
    elif searchType == 'dishes':
        dishes = Product.query.filter(Product.product_name.like('%' + searchKey + '%') if searchKey is not None else "").all()
        result = list()
        for dish in dishes:
            shop = Shop.query.filter_by(shop_id=dish.shop_id)
            if shop.shop_status == 'open':
                a = dict()
                a['product_id'] = dish.product_id
                a['shop_id'] = dish.shop_id
                a['product_name'] = dish.product_name
                a['product_info'] = dish.product_info
                a['total_sale'] = dish.total_sale
                result.append(a)
            else: continue
        return Response(json.dumps(result),  mimetype='application/json')

@api_bp.route('/order_management',methods=['GET','POST'])
def shop_orders():
    response_object = {"list":list()}
    if request.method == 'GET':
        shop_id = request.args.get("shop_id")
        orders = Order.query.filter_by(shop_id=shop_id).order_by(Order.create_time.desc()).all()
        # if orders == None:
        #     return jsonify(message=("Orders empty.")), 400
        for i in range(len(orders)):
            order = orders[i]
            info = {
                'key': i,
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

@api_bp.route('/order_detail',methods=['GET','POST'])
def shop_order_detail():
    response_object = {"list":list()}
    if request.method == 'GET':
        order_id = request.args.get("order_id")
        products = Purchased_Product.query.filter_by(order_id=order_id).all()
        if products == None:
            return jsonify(message=("Request id do not exist.")), 404
        for i in range(len(products)):
            info = dict()
            product = products[i]
            info['key'] = i
            info["product_name"] = product.product_name
            info["product_price"] = product.product_price
            info["quantity"] = product.quantity
            response_object['list'].append(info)
        return jsonify(data=response_object)

@api_bp.route('/my_orders',methods=['GET','POST'])
def my_orders():
    response_object = {"list":list()}
    if request.method == 'GET':
        user_id = request.args.get("user_id")
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.create_time.desc()).all()
        for i in range(len(orders)):
            order = orders[i]
            info = {
                'key': i,
                "order_id" : order.order_id,
                "shop_id" : order.shop_id,
                "shop_name" : Shop.query.filter_by(shop_id=order.shop_id).first().shop_name,
                "user_contact": order.user_contact,
                "user_location" : order.user_location,
                "delivery_fee" : order.delivery_fee,
                "create_time": order.create_time,
                "order_status": order.order_status
            }
            response_object['list'].append(info)
        return jsonify(data=response_object)

@api_bp.route('/cancel_order',methods=['POST'])
def cancel_order():
    response_object = dict()
    request_object = request.get_json()
    if request_object is None:
        return jsonify(message=('Invalid item body.')), 400
    order_id = request_object.get("order_id")
    order = Order.query.filter_by(order_id=order_id).first()
    order.order_status = "cancelled"
    db.session.commit()
    response_object["message"] = "Successfully cancel order!"
    return jsonify(data=response_object)

@api_bp.route('/pay_order',methods=['POST'])
def pay_order():
    response_object = dict()
    request_object = request.get_json()
    if request_object is None:
        return jsonify(message=('Invalid item body.'))
    order_id = request_object.get("order_id")
    price = request_object.get("price")
    order = Order.query.filter_by(order_id=order_id).first()
    print(order_id, price, order.order_status)
    if order.order_status != 'approved' and order.order_status != 'delivering':
        return jsonify(message=('Invalid order status.'))
    order.order_status = "finished"
    # transaction of balance
    user_id = order.user_id
    user = User.query.filter_by(user_id=user_id).first()
    shop = Shop.query.filter_by(shop_id=order.shop_id).first()
    user.frozen_balance -= price
    shop.shop_balance += price
    db.session.commit()
    response_object["message"] = "Successfully pay order!"
    return jsonify(data=response_object)

@api_bp.route('/rate_order',methods=['POST'])
def rate_order():
    response_object = dict()
    request_object = request.get_json()
    if request_object is None:
        return jsonify(message=('Invalid item body.')), 400
    shop = Shop.query.filter_by(shop_id=request_object.get('shop_id')).first()
    shop.shop_rate_total += request_object.get("rate")
    shop.shop_rate_number += 1
    db.session.commit()
    response_object["message"] = "Successfully updating rate!"
    return jsonify(data=response_object)

@api_bp.route('/change_order_status',methods=['POST'])
def change_order_status():
    response_object = dict()
    request_object = request.get_json()
    if request_object is None:
        return jsonify(message=('Invalid item body.')), 400
    order_id = request_object.get("order_id")
    status = request_object.get("status")
    current_status = Order.query.filter_by(order_id=order_id).first().order_status
    print(order_id, status, current_status)
    if current_status == "finished" or current_status == "cancelled" or current_status == "denied" or current_status == 'delivering':
        return jsonify(message=("Invalid order status. Can't change status now."))
    if current_status == "pending" and (status != "approved" and status != "denied"):
        return jsonify(message=('Invalid order status. Must approve or deny a pending status.'))
    if current_status == "approved" and status != 'delivering':
        return jsonify(message=('Invalid order status. Can just change to delivering state.'))
    order = Order.query.filter_by(order_id=order_id).first()
    order.order_status = status
    db.session.commit()
    response_object["message"] = "Successfully updating status!"
    return jsonify(data=response_object)

#API for admin
#provide admin application
@api_bp.route('/getOpenApplication', methods=['GET'])
def api_getOpenApplication():
    message = Application.query.filter_by(application_type='open', application_status='pending').all()
    if len(message) == 0:
        return jsonify({})
    else:
        result = list()
        key = 1
        for application in message:
            temp = dict()
            temp['key'] = key
            temp['application_id'] = application.application_id
            temp['user_id'] = application.user_id
            temp['shop_name'] = application.shop_name
            temp['contact'] = application.shop_contact
            temp['location'] = application.shop_location
            temp['detail_location'] = application.shop_location_detail
            temp['license'] = application.shop_license_number
            temp['info'] = application.shop_info
            result.append(temp)
            key += 1
        return Response(json.dumps(result), mimetype='application/json')

@api_bp.route('/getCloseApplication', methods=['GET'])
def api_getCloseApplication():
    message = Application.query.filter_by(application_type='cancel', application_status='pending').all()
    if len(message) == 0:
        return jsonify({})
    else:
        result = list()
        key = 1
        for application in message:
            temp = dict()
            temp['key'] = key
            temp['application_id'] = application.application_id
            temp['user_id'] = application.user_id
            temp['shop_id'] = application.shop_id
            temp['shop_name'] = application.shop_name
            temp['license'] = application.shop_license_number
            temp['info'] = application.shop_info
            result.append(temp)
            key += 1
        return Response(json.dumps(result), mimetype='application/json')

@api_bp.route('/getUnblockApplication', methods=['GET'])
def api_getUnblockApplication():
    message = Application.query.filter_by(application_type='unblock', application_status='pending').all()
    if len(message) == 0:
        return jsonify({})
    else:
        result = list()
        key = 1
        for application in message:
            temp = dict()
            temp['key'] = key
            temp['application_id'] = application.application_id
            temp['user_id'] = application.user_id
            temp['shop_id'] = application.shop_id
            temp['shop_name'] = application.shop_name
            temp['license'] = application.shop_license_number
            result.append(temp)
            key += 1
        return Response(json.dumps(result), mimetype='application/json')

#application operation
@api_bp.route('/operateApplication', methods=['POST'])
def api_operateApplication():
    data = request.get_json()
    op_type = data['op_type']
    app_id = data['app_id']
    application = Application.query.get(app_id)
    if op_type == 'denied' :
        db.session.commit()
        return jsonify({
            'status': 'ok',
            'info': 'Denied success!'
        })
    else: #if approve
        app_type = application.application_type
        application.application_status = 'approved'
        if app_type == 'open':
            # create shop
            user_id = application.user_id
            shop_name = application.shop_name
            shop_info = application.shop_info
            shop_contact = application.shop_contact
            shop_location = application.shop_location
            shop_location_detail = application.shop_location_detail
            shop_license = application.shop_license_number
            shop = Shop(user_id=user_id, shop_name=shop_name,
            shop_info=shop_info, shop_contact=shop_contact,
            shop_location=shop_location, shop_location_detail=shop_location_detail,
            shop_license_number=shop_license, shop_status='open',shop_balance=0)
            db.session.add(shop)
            db.session.commit()
            return jsonify({'status': 'ok', 'info':'approve success'})
        if app_type == 'cancel':
            shop_id = application.shop_id
            shop = Shop.query.get(shop_id)
            shop.shop_status = 'cancelled'
            db.session.commit()
            return jsonify({'status': 'ok', 'info': 'cancel success'})
        if app_type == 'unblock':
            shop_id = application.shop_id
            shop = Shop.query.get(shop_id) 
            shop.shop_status = 'open'
            db.session.commit()
            return jsonify({'status': 'ok', 'info': 'unblock success'})

#get user info
@api_bp.route('/getUser', methods=['GET'])
def api_getUser():
    messages = User.query.all()
    if len(messages) == 0:
        return jsonify({})
    else:
        result = list()
        key = 1
        for user in messages:
            temp = dict()
            temp['key'] = key
            temp['user_id'] = user.user_id
            temp['user_name'] = user.user_name
            result.append(temp)
            key += 1
        return Response(json.dumps(result), mimetype='application/json')

#search user info
@api_bp.route('/searchUser', methods=['GET'])
def api_searchUser():
    data = request.args.get('id')
    message = User.query.get(data)
    if message == None:
        return jsonify({})
    else:
        result = list()
        temp = dict()
        temp['key'] = 1
        temp['user_id'] = message.user_id
        temp['user_name'] = message.user_name
        result.append(temp)
        return Response(json.dumps(result), mimetype='application/json')

#get shop info
@api_bp.route('/getAllShop', methods=['GET'])
def api_getShop():
    messages = Shop.query.all()
    if len(messages) == 0:
        return jsonify({})
    else:
        result = list()
        key = 1
        for shop in messages:
            temp = dict()
            temp['key'] = key
            temp['shop_id'] = shop.shop_id
            temp['shop_name'] = shop.shop_name
            temp['shop_status'] = shop.shop_status
            temp['shop_location'] = shop.shop_location
            temp['shop_info'] = shop.shop_info
            result.append(temp)
            key += 1
        return Response(json.dumps(result), mimetype='application/json')

#search shop info
@api_bp.route('/searchShop', methods=['GET'])
def api_searchShop():
    data = request.args.get('id')
    message = Shop.query.get(data)
    if message == None:
        return jsonify({})
    else:
        result = list()
        temp = dict()
        temp['key'] = 1
        temp['shop_id'] = message.shop_id
        temp['shop_name'] = message.shop_name
        temp['shop_status'] = message.shop_status
        temp['shop_location'] = message.shop_location
        temp['shop_info'] = message.shop_info
        temp['shop_rate'] = message.shop_rate_number
        temp['delivery_fee'] = message.shop_delivery_fee
        result.append(temp)
        return Response(json.dumps(result), mimetype='application/json')

#block shop
@api_bp.route('/blockShop', methods=['POST'])
def api_blockShop():
    data = request.get_json()
    shop_id = data['shop_id']
    shop = Shop.query.get(shop_id)
    shop.shop_status = 'blocked'
    db.session.commit()
    return jsonify({'status': 'ok', 'info': 'block success'})

#unblock shop
@api_bp.route('/unblockShop', methods=['POST'])
def api_unblockShop():
    data = request.get_json()
    shop_id = data['shop_id']
    shop = Shop.query.get(shop_id)
    shop.shop_status = 'open'
    db.session.commit()
    return jsonify({'status': 'ok', 'info': 'unblock success'})

#get order info
@api_bp.route('/getAllOrder', methods=['GET'])
def api_getOrder():
    # result = list()
    # temp = dict()
    # temp['key'] = 1
    # temp['order_id'] = 1
    # temp['user_id'] = 1
    # temp['shop_id'] = 1
    # purchased_products = list()
    # purchased_products.append(('dishes1',1))
    # purchased_products.append(('dishes2',1))
    # temp['purchased_products'] = purchased_products
    # temp['user_contact'] = '12345678901'
    # temp['user_location'] = 'order.user_location'
    # temp['delivery_fee'] = 1
    # temp['create_time'] = "yyyy-mm-dd h:m:s"
    # temp['order_status'] = 'pending'
    # result.append(temp)
    # return Response(json.dumps(result), mimetype='application/json')


    messages = Order.query.all()
    if len(messages) == 0:
        return jsonify({})
    else:
        result = list()
        key = 1
        for order in messages:
            temp = dict()
            temp['key'] = key
            temp['order_id'] = order.order_id
            temp['user_id'] = order.user_id
            temp['shop_id'] = order.shop_id
            purchased_products = list()
            # products = Purchased_Product.query.filter_by(order_id=order.order_id)
            # for product in products:
            #     product_name = product.product_name
            #     product_quantity = product.product_quantity
            #     purchased_products.append((product_name,product_quantity))
            temp['purchased_products'] = purchased_products
            temp['user_contact'] = order.user_contact
            temp['user_location'] = order.user_location
            temp['delivery_fee'] = order.delivery_fee
            temp['create_time'] = order.create_time.strftime("%Y-%m-%d %H:%M:%S")
            temp['order_status'] = order.order_status
            result.append(temp)
            key += 1
        return Response(json.dumps(result), mimetype='application/json')

#search order info
@api_bp.route('/searchOrder', methods=['GET'])
def api_searchOrder():
    data = request.args.get('id')
    message = Order.query.get(data)
    if message == None:
        return jsonify({})
    else:
        result = list()
        temp = dict()
        temp['key'] = 1
        temp['order_id'] = message.order_id
        temp['user_id'] = message.user_id
        temp['shop_id'] = message.shop_id
        purchased_products = list()
        products = Purchased_Product.query.filter_by(order_id=message.order_id)
        for product in products:
            product_name = product.product_name
            product_quantity = product.product_quantity
            purchased_products.append((product_name,product_quantity))
        temp['purchased_products'] = purchased_products
        temp['user_contact'] = message.user_contact
        temp['user_location'] = message.user_location
        temp['delivery_fee'] = message.delivery_fee
        temp['create_time'] = message.create_time
        temp['order_status'] = message.order_status
        result.append(temp)
        return Response(json.dumps(result), mimetype='application/json')

#get a shop's dishes info 
@api_bp.route('/getDishesInfo', methods=['GET'])
def api_getDishesInfo():
    data = request.args.get('id')
    shop = Shop.query.get(data)
    dishes = Product.query.filter_by(shop_id=data).all()
    result = list()
    for i in dishes:
        a = dict()
        a['productid'] = i.product_id
        a['name'] = i.product_name
        a['info'] = i.product_info
        a['price'] = i.product_price
        a['sale'] = i.total_sale
        a['count'] = 0
        result.append(a)
    return Response(json.dumps(result),  mimetype='application/json')

#submit order
@api_bp.route('/submitOrder', methods=['POST'])
def api_submitOrder():
    data = request.get_json()
    dishes = data['dishes']
    shop_id = int(data['shop_id'])
    user_id = int(data['user_id'])
    price = data['price']
    user_contact = data['user_contact']
    user_location = data['user_location']
    delivery_fee = int(data['delivery_fee'])
    # print(shop_id,user_id,user_contact,user_location,delivery_fee)
    #change fund
    user = User.query.get(user_id)
    user.available_balance = round(user.available_balance - price, 2)
    frozen_balance = user.frozen_balance
    user.frozen_balance =frozen_balance + price
    #create order
    order = Order(
        # order_id = 0,
        shop_id=shop_id, 
        user_id=user_id, 
        user_contact=user_contact,
        user_location=user_location,
        delivery_fee=delivery_fee,
        create_time=datetime.utcnow(),
        order_status='pending'
    )
    db.session.add(order)

    # message = Order.query.all()
    # for order in message:
    #     print(order.shop_id)
    # add products
    for dish in dishes:
        # print(type(dish))
        product_id = dish['id']
        product_name = dish['name']
        product_quantity = dish['quantity']
        product_price = dish['price']
        product = Purchased_Product(
            product_id = product_id,
            product_name = product_name,
            product_price = product_price,
            quantity = product_quantity,
        )
        db.session.add(product)
        order.purchased_products.append(product)
    db.session.commit()
    # print(type(dishes))
    # print(user_id)
    # print(shop_id)
    return jsonify({'status': 'ok', 'info': 'submit success'})