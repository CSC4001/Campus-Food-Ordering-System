# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import flash, redirect, url_for, render_template, abort, Blueprint
from shop_and_admin.shopSystem.extensions import db
from shop_and_admin.shopSystem.models import *
from shop_and_admin.shopSystem.forms import *

# from shopSystem import app, db
# from shopSystem.forms import ShopInfoForm, ProductInfoForm, DeleteForm
# from shopSystem.models import Shop, Product

shopSystem_bp = Blueprint("shopSystem",__name__, static_folder='shopSystem/static', template_folder='shopSystem/templates')


# TODO: need connection to user system
# TODO: jsonify everything
'''
index route "/" : display the shop_and_admin in the database
'''
# TODO: Display according to shop_and_admin owners
# TODO: Add application of adding new shops
@shopSystem_bp.route('/', methods=['GET', 'POST'])
def index():
    messages = Shop.query.order_by(Shop.shop_name.desc()).all()
    return render_template('index.html', messages=messages)

'''
shop_and_admin index route "/shop_<int:shop_id>" : display shop_and_admin information
'''
@shopSystem_bp.route('/shop_<int:shop_id>')
def shop_index(shop_id):
    message = Shop.query.filter_by(shop_id=shop_id).first()
    return render_template('shop_index.html', message=message)


'''
edit route "/shop_<int:shop_id>/edit" : edit shop_and_admin information
'''
# TODO: need to add application of pending / undo pending
@shopSystem_bp.route('/shop_<int:shop_id>/edit', methods=['GET', 'POST'])
def edit_shop(shop_id):
    # if shop_and_admin is closed, cannot enter this page
    form = ShopInfoForm()
    shop = Shop.query.get(shop_id)
    if shop.shop_status == '已关店':
        flash('该店铺已关闭。')
        return redirect(url_for('shopSystem.index'))
    if form.validate_on_submit():
        shop.shop_name = form.shop_name.data
        shop.shop_contact = form.shop_contact.data
        shop.shop_location = form.shop_location.data
        shop.shop_location_detail = form.shop_location_detail.data
        shop.shop_license_number = form.shop_license_number.data
        shop.shop_info = form.shop_info.data
        shop.shop_delivery_fee = form.shop_delivery_fee.data
        if shop.shop_status == '停业整顿':
            flash('当前状态无法操作。请联系管理员申请复业。')
            return redirect(url_for('shopSystem.edit_shop',shop_id=shop_id))
        else:
            shop.shop_status = form.shop_status.data
        db.session.commit()
        flash('Successful update to shop_and_admin info!')
        return redirect(url_for('shopSystem.shop_index',shop_id=shop_id))
    form.shop_name.data = shop.shop_name
    form.shop_contact.data = shop.shop_contact
    form.shop_location.data = shop.shop_location
    form.shop_location_detail.data = shop.shop_location_detail
    form.shop_license_number.data = shop.shop_license_number
    form.shop_info.data = shop.shop_info
    form.shop_delivery_fee.data = form.shop_delivery_fee.choices[int(shop.shop_delivery_fee)][0]
    form.shop_status.data = shop.shop_status
    return render_template('edit_shop.html', form=form, shop_id=shop_id)

'''
dishes management route "/shop_<int:shop_id>/dishes" : displaying dishes of a shop_and_admin
'''
# TODO: did not specify searching function in this page
@shopSystem_bp.route('/shop_<int:shop_id>/dishes')
def dishes(shop_id):
    form = DeleteForm()
    messages = Product.query.filter_by(shop_id=shop_id).all()
    return render_template('dishes.html',messages=messages, shop_id=shop_id,form=form)

'''
dishes adder route "/shop_<int:shop_id>/dish_<int:product_id>/add : adding a dish
'''
@shopSystem_bp.route('/shop_<int:shop_id>/add', methods=['GET', 'POST'])
def add_dish(shop_id):
    form = ProductInfoForm()
    if form.validate_on_submit():
        product_name = form.product_name.data
        product_price = form.product_price.data
        product_info = form.product_info.data
        product = Product(
            shop_id=shop_id,
            product_name=product_name,
            product_price=product_price,
            product_info=product_info,
            total_sale=0
        )
        db.session.add(product)
        product.shop=Shop.query.get(shop_id)
        db.session.commit()
        flash('成功加入新菜品!')
        return redirect(url_for('shopSystem.dishes',shop_id=shop_id))
    return render_template('add_dish.html', form=form, shop_id=shop_id)

'''
dishes editor route "/shop_<int:shop_id>/dish_<int:product_id>/edit : edit info of a dish
'''
@shopSystem_bp.route('/shop_<int:shop_id>/dish_<int:product_id>/edit', methods=['GET', 'POST'])
def edit_dish(shop_id, product_id):
    form = ProductInfoForm()
    product = Product.query.get(product_id)
    if form.validate_on_submit():
        product.product_name = form.product_name.data
        product.product_price = form.product_price.data
        product.product_info = form.product_info.data
        db.session.commit()
        flash('成功修改菜品信息！')
        return redirect(url_for('shopSystem.dishes',shop_id=shop_id))
    form.product_info.data = product.product_info
    form.product_price.data = product.product_price
    form.product_name.data = product.product_name
    return render_template('edit_dish.html',form=form,shop_id=shop_id)

'''
dishes deletor route "/shop_<int:shop_id>/dish_<int:product_id>/delete : delete a dish
'''
@shopSystem_bp.route('/shop_<int:shop_id>/dish_<int:product_id>/delete', methods=['POST'])
def delete_dish(shop_id,product_id):
    form = DeleteForm()
    if form.validate_on_submit():
        product = Product.query.get(product_id)
        db.session.delete(product)
        db.session.commit()
        flash('菜品已被删除！')
    else:
        abort(400)
    return redirect(url_for('shopSystem.dishes',shop_id=shop_id))

'''
@shopSystem_bp.route('/add/<int:shop_id>', methods=['GET', 'POST'])
def edit_note(shop_id):
    form = ShopInfoForm()
    shop_and_admin = Shop.query.get(shop_id)
    if form.validate_on_submit():
        shop_name = form.shop_name.data
        shop_contact = form.shop_contact.data
        shop_location = form.shop_location.data
        shop_location_detail = form.shop_location_detail.data
        shop_license_number = form.shop_license_number.data
        shop_info = form.shop_info.data
        message = Shop( shop_name = shop_name,
                        shop_contact = shop_contact,
                        shop_location = shop_location,
                        shop_location_detail = shop_location_detail,
                        shop_license_number = shop_license_number,
                        shop_info = shop_info)
        db.session.add(message)
        db.session.commit()
        flash('Successful update to shop_and_admin info!')
        return redirect(url_for('index'))
    return render_template('edit_note.html', form=form)
'''
