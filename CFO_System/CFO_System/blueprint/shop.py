# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import flash, redirect, url_for, render_template, abort, Blueprint
from flask_login import  login_required, current_user
from CFO_System.models import *
from CFO_System.forms import *
from CFO_System.utils import *
from CFO_System.utils import redirect_back

# from CFO_System import app, db
# from CFO_System.forms import ShopInfoForm, ProductInfoForm, DeleteForm
# from CFO_System.models import Shop, Product

shop_bp = Blueprint("shop",__name__)


@shop_bp.before_request
@login_required
def login_protect():
    pass

'''
index route "/" : display the shop in the database
'''
# TODO: Add application of adding new shops, apply to shutdown, apply to unban
@shop_bp.route('/', methods=['GET', 'POST'])
def index():
    messages = Shop.query.filter_by(user_id=current_user.user_id).order_by(Shop.shop_name.desc()).all()
    return render_template('shop/index.html', messages=messages)

'''
shop index route "/shop_<int:shop_id>" : display shop information
'''
@shop_bp.route('/shop_<int:shop_id>')
def shop_index(shop_id):
    # check if have access to the shop
    if not is_my_shop(shop_id):
        return redirect_back()
    else:
        shop = Shop.query.get(shop_id)
        if shop.shop_status == 'cancelled':
            flash('This shop is shut down.')
            return redirect(url_for('shop.index'))
        message = Shop.query.filter_by(shop_id=shop_id).first()
        return render_template('shop/shop_index.html', message=message)


'''
edit route "/shop_<int:shop_id>/edit" : edit shop information
'''
# TODO: need to add application of pending / undo pending
@shop_bp.route('/shop_<int:shop_id>/edit', methods=['GET', 'POST'])
def edit_shop(shop_id):
    # check if have access to the shop
    if not is_my_shop(shop_id):
        return redirect_back()
    else:
        # if shop is closed, cannot enter this page
        form = ShopInfoForm()
        shop = Shop.query.get(shop_id)
        if form.validate_on_submit():
            shop.shop_name = form.shop_name.data
            shop.shop_contact = form.shop_contact.data
            shop.shop_location = form.shop_location.data
            shop.shop_location_detail = form.shop_location_detail.data
            shop.shop_license_number = form.shop_license_number.data
            shop.shop_info = form.shop_info.data
            shop.shop_delivery_fee = form.shop_delivery_fee.data
            if shop.shop_status == 'blocked':
                flash('This shop is blocked. Please contact the administrator.')
                return redirect(url_for('shop.edit_shop',shop_id=shop_id))
            else:
                shop.shop_status = form.shop_status.data
            db.session.commit()
            flash('Successful update to shop info!')
            return redirect(url_for('shop.shop_index',shop_id=shop_id))
        form.shop_name.data = shop.shop_name
        form.shop_contact.data = shop.shop_contact
        form.shop_location.data = shop.shop_location
        form.shop_location_detail.data = shop.shop_location_detail
        form.shop_license_number.data = shop.shop_license_number
        form.shop_info.data = shop.shop_info
        form.shop_delivery_fee.data = form.shop_delivery_fee.choices[int(shop.shop_delivery_fee)][0]
        form.shop_status.data = shop.shop_status
        return render_template('shop/edit_shop.html', form=form, shop_id=shop_id)

'''
dishes management route "/shop_<int:shop_id>/dishes" : displaying dishes of a shop 
'''
# TODO: did not specify searching function in this page
@shop_bp.route('/shop_<int:shop_id>/dishes')
def dishes(shop_id):
    # check if have access to the shop
    if not is_my_shop(shop_id):
        return redirect_back()
    else:
        form = DeleteForm()
        shop = Shop.query.get(shop_id)
        messages = Product.query.filter_by(shop_id=shop_id).all()
        if shop.shop_status == 'blocked':
            flash('This shop is blocked. Please contact the administrator.')
            return redirect(url_for('shop.shop_index',shop_id=shop_id))
        return render_template('shop/dishes.html',messages=messages, shop_id=shop_id,form=form)

'''
dishes adder route "/shop_<int:shop_id>/dish_<int:product_id>/add : adding a dish
'''
@shop_bp.route('/shop_<int:shop_id>/add', methods=['GET', 'POST'])
def add_dish(shop_id):
    # check if have access to the shop
    if not is_my_shop(shop_id):
        return redirect_back()
    else:
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
            return redirect(url_for('shop.dishes',shop_id=shop_id))
        return render_template('shop/add_dish.html', form=form, shop_id=shop_id)

'''
dishes editor route "/shop_<int:shop_id>/dish_<int:product_id>/edit : edit info of a dish
'''
@shop_bp.route('/shop_<int:shop_id>/dish_<int:product_id>/edit', methods=['GET', 'POST'])
def edit_dish(shop_id, product_id):
    # check if have access to the shop
    if not is_my_shop(shop_id):
        return redirect_back()
    else:
        form = ProductInfoForm()
        product = Product.query.get(product_id)
        if form.validate_on_submit():
            product.product_name = form.product_name.data
            product.product_price = form.product_price.data
            product.product_info = form.product_info.data
            db.session.commit()
            flash('成功修改菜品信息！')
            return redirect(url_for('shop.dishes',shop_id=shop_id))
        form.product_info.data = product.product_info
        form.product_price.data = product.product_price
        form.product_name.data = product.product_name
        return render_template('shop/edit_dish.html',form=form,shop_id=shop_id)

'''
dishes deletor route "/shop_<int:shop_id>/dish_<int:product_id>/delete : delete a dish
'''
@shop_bp.route('/shop_<int:shop_id>/dish_<int:product_id>/delete', methods=['POST'])
def delete_dish(shop_id,product_id):
    # check if have access to the shop
    if not is_my_shop(shop_id):
        return redirect_back()
    else:
        form = DeleteForm()
        if form.validate_on_submit():
            product = Product.query.get(product_id)
            db.session.delete(product)
            db.session.commit()
            flash('菜品已被删除！')
        else:
            abort(400)
        return redirect(url_for('shop.dishes',shop_id=shop_id))

'''
route for applying a new shop
'''
@shop_bp.route('/apply_new_shop', methods=['GET', 'POST'])
def apply_new_shop():
    # if shop is closed, cannot enter this page
    form = ShopAddingForm()
    if form.validate_on_submit():
        shop_name = form.shop_name.data
        shop_contact = form.shop_contact.data
        shop_location = form.shop_location.data
        shop_location_detail = form.shop_location_detail.data
        shop_license_number = form.shop_license_number.data
        shop_info = form.shop_info.data
        application = Application(
            user_id=current_user.user_id,
            application_type="open",
            shop_name = shop_name,
            shop_contact = shop_contact,
            shop_license_number = shop_license_number,
            shop_location = shop_location,
            shop_location_detail = shop_location_detail,
            shop_info=shop_info,
            application_status="pending"
        )
        db.session.add(application)
        db.session.commit()
        flash('Successfully submitted the open shop application!')
        return redirect(url_for('shop.index'))

    return render_template('shop/apply_new_shop.html', form=form)

'''
route for applying cancelling, namely shutting down the shop permanently
'''
@shop_bp.route('/shop_<int:shop_id>/apply_cancel', methods=['GET', 'POST'])
def apply_cancel(shop_id):
    # check if have access to the shop
    if not is_my_shop(shop_id):
        return redirect_back()
    else:
        shop = Shop.query.filter_by(shop_id=shop_id).first()
        if shop.shop_status == 'cancelled' or shop.shop_status == 'blocked':
            flash("Cannot do this operation.")
            return redirect_back()
        application = Application(
            user_id=current_user.user_id,
            shop_id=shop.shop_id,
            application_type="cancel",
            shop_name = shop.shop_name,
            shop_license_number = shop.shop_license_number,
            application_status="pending"
        )
        db.session.add(application)
        db.session.commit()
        flash('Successfully submitted the cancelling shop application!')
        return redirect(url_for('shop.index'))

'''
route for applying unblock the shop
'''
@shop_bp.route('/shop_<int:shop_id>/apply_unblock', methods=['GET', 'POST'])
def apply_unblock(shop_id):
    # check if have access to the shop
    if not is_my_shop(shop_id):
        return redirect_back()
    else:
        shop = Shop.query.filter_by(shop_id=shop_id).first()
        if shop.shop_status != "blocked":
            flash("Cannot do this operation.")
            return redirect_back()
        application = Application(
            user_id=current_user.user_id,
            shop_id=shop.shop_id,
            application_type="unblock",
            shop_name = shop.shop_name,
            shop_license_number = shop.shop_license_number,
            application_status="pending"
        )
        db.session.add(application)
        db.session.commit()
        flash('Successfully submitted the unblock shop application!')
        return redirect(url_for('shop.index'))


