# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import flash, redirect, url_for, render_template

from shopSystem import app, db
from shopSystem.forms import ShopInfoForm
from shopSystem.models import Shop

# TODO: need connection to user system
# TODO: jsonify everything
'''
index route "/" : display the shop in the database
TODO:
1. Display according to shop owners
2. Add product managements
3. Add application of adding new shops
'''
@app.route('/', methods=['GET', 'POST'])
def index():
    messages = Shop.query.order_by(Shop.shop_name.desc()).all()
    return render_template('index.html', messages=messages)

'''
edit route "/edit/shop_id" : edit shop information
TODO:
1. need to add application of pending / undo pending
'''
@app.route('/edit/<int:shop_id>', methods=['GET', 'POST'])
def edit_shop(shop_id):
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
        db.session.commit()
        flash('Successful update to shop info!')
        return redirect(url_for('index'))
    form.shop_name.data = shop.shop_name
    form.shop_contact.data = shop.shop_contact
    form.shop_location.data = shop.shop_location
    form.shop_location_detail.data = shop.shop_location_detail
    form.shop_license_number.data = shop.shop_license_number
    form.shop_info.data = shop.shop_info
    form.shop_delivery_fee.data = form.shop_delivery_fee.choices[int(shop.shop_delivery_fee)][0]
    return render_template('edit.html', form=form)

'''
@app.route('/add/<int:shop_id>', methods=['GET', 'POST'])
def edit_note(shop_id):
    form = ShopInfoForm()
    shop = Shop.query.get(shop_id)
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
        flash('Successful update to shop info!')
        return redirect(url_for('index'))
    return render_template('edit_note.html', form=form)
'''
