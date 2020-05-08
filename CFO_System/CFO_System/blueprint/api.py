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

# create open shop application
@api_bp.route('/submitShopOpenApplication', methods=['POST'])
def api_submitShopOpenApplciation():
    data = request.get_json()
    user_id = data['id']
    app_type='open'
    shop_id = -1
    name = data['name']
    info = data['info']
    contact = data['contact']
    location_detail = data['locationDetail']
    license_number = data['licenseNum']
    app_status = 'pending'
    application = Application(user_id=user_id,application_type=app_type,
    shop_id=shop_id, shop_name=name, shop_info=info, shop_contact=contact,
    shop_location_detail=location_detail, shop_license_number=license_number,
    application_status=app_status)
    db.session.add(application)
    db.session.commit()
    test = Application.query.filter_by(user_id=user_id).first()
    if test.user_name == username:
        return jsonify({'status':'ok','info':'submit successfully'})
    return jsonify({'status':'no','info':'submit failure'})

# provide admin application
@api_bp.route('/getApplication', methods=['GET'])
def api_getApplication():
    data = request.args.get('type')
    message = Application.query.filter_by(application_type=data, application_status='pending').all()
    if len(message) == 0:
        return jsonify({})
    else:
        result = list()
        for application in message:
            temp = dict()
            temp['application_id'] = application.application_id
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
            # temp['contact'] = application.shop_contact
            # temp['location'] = application.shop_location
            temp['license'] = application.shop_license_number
            result.append(temp)
        return Response(json.dumps(result), mimetype='application/json')

#application operation
@api_bp.route('/operateApplication', methods=['POST'])
def api_operateApplication():
    # app_id = request.args.get(app_id)
    data = request.get_json()
    op_type = data['op_type']
    app_id = data['app_id']
    application = Application.query.get(app_id)
    if op_type == 'denied' :
        # application.application_status = 'denied'
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
            shop_license_number=shop_license, shop_status='open',)
            db.session.add(shop)
            # db.add(shop)
            # db.commit()
            db.session.commit()
            return jsonify({'status': 'ok', 'info':'approve success'})
        if app_type == 'cancel':
            shop_id = application.shop_id
            shop = Shop.query.get(shop_id)
            shop.shop_status = 'cancelled'
            db.session.commit()
            return jsonify({'status': 'ok', 'info': 'cancel success'})

#get user info
@api_bp.route('/getUser', methods=['GET'])
def api_getUser():
    messages = User.query.all()
    # result = [0,1]
    if len(messages) == 0:
        return jsonify({})
    # return Response(json.dumps(result),mimetype='application/json')
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

