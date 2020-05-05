# -*- coding: utf-8 -*-

from flask import flash, redirect, url_for, render_template, session, abort

from customer_system import app, db
from customer_system.forms import *
from customer_system.models import *


shop_locations = ['Student_Center', 'Shaw_College', 'Deligentia_College', 'Le_Tian_Building']


@app.route('/', methods=['GET', 'POST'])
def index():
    '''Display the index page'''
    welcome = 'Welcome!'
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        welcome += ' ID: {} Name: {}'.format(user.user_id, user.user_name)
    search_form = SearchForm()
    logout_form = LogoutForm()
    if search_form.search.data and search_form.validate_on_submit():
        shops = Shop.query.filter(Shop.shop_name.like('%{}%'.format(search_form.keyword.data))).all()
        shops = sorted(shops, key=lambda x: x.shop_rate_total / x.shop_rate_number if x.shop_rate_number else 0, reverse=True)
        products = Product.query.filter(Product.product_name.like('%{}%'.format(search_form.keyword.data))).all()
        products = sorted(products, key=lambda x: x.total_sale, reverse=True)
        return render_template('index.html', search_form=search_form, logout_form=logout_form, welcome=welcome, shops=shops, products=products)
    if logout_form.submit_logout.data and logout_form.validate_on_submit():
        if 'user_id' in session:
            session.pop('user_id')
            flash('You have successfully signed out!')
        return redirect(url_for('index'))
    shops = Shop.query.all()
    shops = sorted(shops, key=lambda x: x.shop_rate_total / x.shop_rate_number if x.shop_rate_number else 0, reverse=True)
    products = []
    for shop in shops:
        products += shop.products
    products = sorted(products, key=lambda x: x.total_sale, reverse=True)
    return render_template('index.html', search_form=search_form, logout_form=logout_form, welcome=welcome, shops=shops, products=products)


@app.route('/<any({}):location>'.format(str(shop_locations)[1:-1]), methods=['GET', 'POST'])
def location(location):
    welcome = 'Welcome!'
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        welcome += ' ID: {} Name: {}'.format(user.user_id, user.user_name)
    search_form = SearchForm()
    logout_form = LogoutForm()
    if search_form.search.data and search_form.validate_on_submit():
        shops = Shop.query.filter(Shop.shop_name.like('%{}%'.format(search_form.keyword.data)), Shop.shop_location == location.replace('_',' ')).all()
        shops = sorted(shops, key=lambda x: x.shop_rate_total / x.shop_rate_number if x.shop_rate_number else 0, reverse=True)
        results = Product.query.filter(Product.product_name.like('%{}%'.format(search_form.keyword.data))).all()
        products = []
        for product in results:
            if product.shop.shop_location == location.replace('_',' '):
                products.append(product)
        products = sorted(products, key=lambda x: x.total_sale, reverse=True)
        return render_template('index.html', search_form=search_form, logout_form=logout_form, welcome=welcome, shops=shops, products=products)
    if logout_form.submit_logout.data and logout_form.validate_on_submit():
        if 'user_id' in session:
            session.pop('user_id')
            flash('You have successfully signed out!')
        return redirect(url_for('index'))
    shops = Shop.query.filter_by(shop_location=location.replace('_',' ')).all()
    shops = sorted(shops, key=lambda x: x.shop_rate_total / x.shop_rate_number if x.shop_rate_number else 0, reverse=True)
    products = []
    for shop in shops:
        products += shop.products
    products = sorted(products, key=lambda x: x.total_sale, reverse=True)
    return render_template('index.html', search_form=search_form, logout_form=logout_form, welcome=welcome, shops=shops, products=products)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Display the login form and set cookie if login succeeds'''
    login_form = LoginForm()
    if login_form.submit.data and login_form.validate_on_submit():
        email = login_form.email.data
        user_password = login_form.user_password.data
        result = User.query.filter(User.email==email, User.user_password==user_password).all()
        if len(result) > 1:
            abort(500)
        if result:
            if result[0].user_status == 'blocked':
                flash('The account is blocked!')
                return redirect(url_for('index'))
            session['user_id'] = result[0].user_id
            flash('You have successfully signed in!')
            return redirect(url_for('index'))
        flash('Account does not exist or password is wrong!')
        return redirect(url_for('login'))
    return render_template('login.html', login_form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Display the register form and check for duplications'''
    register_form = RegisterForm()
    if register_form.submit.data and register_form.validate_on_submit():
        email = register_form.email.data
        user_password = register_form.user_password.data
        result = User.query.filter(User.email==email).all()
        if result:
            flash('The email address has already been registered!')
            return redirect(url_for('register'))
        user = User(
            email = email,
            user_password = user_password,
            user_name = 'Unnamed User',
            user_avatar = None,
            user_contact = '',
            available_balance = 0,
            frozen_balance = 0,
            user_status = 'normal'
        )
        db.session.add(user)
        db.session.commit()
        flash('You have successfully registered!')
        return redirect(url_for('index'))
    return render_template('register.html', register_form=register_form)


@app.route('/personal_center', methods=['GET', 'POST'])
def personal_center():
    '''Check login status and display the forms in the personal center page'''
    if 'user_id' not in session:
        abort(404)
    user = User.query.get(session['user_id'])
    bookmarks = user.bookmarked_shops

    password_form = PasswordForm()
    name_form = NameForm()
    contact_form = ContactForm()
    deposit_form = DepositForm()
    withdraw_form = WithdrawForm()

    if password_form.submit_password.data and password_form.validate_on_submit():
        user.user_password = password_form.user_password.data
        db.session.commit()
        flash('You have successfully changed your password!')
        return redirect(url_for('personal_center'))

    if name_form.submit_name.data and name_form.validate_on_submit():
        user.user_name = name_form.user_name.data
        db.session.commit()
        flash('You have successfully changed your name!')
        return redirect(url_for('personal_center'))

    if contact_form.submit_contact.data and contact_form.validate_on_submit():
        user.user_contact = contact_form.user_contact.data
        db.session.commit()
        flash('You have successfully changed your contact!')
        return redirect(url_for('personal_center'))

    if deposit_form.submit_deposit.data and deposit_form.validate_on_submit():
        amount = round(deposit_form.deposit_amount.data, 2)
        if user.available_balance + amount <= 10000:
            user.available_balance = round(user.available_balance + amount, 2)
            db.session.commit()
            flash('You have successfully deposited {}!'.format(amount))
        else:
            flash('Exceed maximum balance limit!')
        return redirect(url_for('personal_center'))

    if withdraw_form.submit_withdraw.data and withdraw_form.validate_on_submit():
        amount = round(withdraw_form.withdraw_amount.data, 2)
        if user.available_balance - amount >= 0:
            user.available_balance = round(user.available_balance - amount, 2)
            db.session.commit()
            flash('You have successfully withdrew {}!'.format(amount))
        else:
            flash('Insufficient funds!')
        return redirect(url_for('personal_center'))

    name_form.user_name.data = user.user_name
    contact_form.user_contact.data = user.user_contact
    return render_template('personal_center.html', user=user,
        password_form=password_form, name_form=name_form, contact_form=contact_form,
        deposit_form=deposit_form, withdraw_form=withdraw_form, bookmarks=bookmarks
    )


@app.route('/shop_<int:shop_id>', methods=['GET', 'POST'])
def view_shop(shop_id):
    welcome = 'Welcome!'
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        welcome += ' ID: {} Name: {}'.format(user.user_id, user.user_name)
    shop = Shop.query.get(shop_id)
    products = shop.products

    logout_form = LogoutForm()
    add_bookmark_form = AddBookmarkForm()
    delete_bookmark_form = DeleteBookmarkForm()

    if logout_form.submit_logout.data and logout_form.validate_on_submit():
        if 'user_id' in session:
            session.pop('user_id')
            flash('You have successfully signed out!')
        return redirect(url_for('index'))

    if add_bookmark_form.submit_add_bookmark.data and add_bookmark_form.validate_on_submit():
        if 'user_id' not in session:
            flash('You need to log in first!')
            return redirect(url_for('view_shop', shop_id=shop_id))
        if shop not in user.bookmarked_shops:
            user.bookmarked_shops.append(shop)
            db.session.commit()
            flash('You have successfully add the shop to your bookmarks!')
        return redirect(url_for('view_shop', shop_id=shop_id))

    if delete_bookmark_form.submit_delete_bookmark.data and delete_bookmark_form.validate_on_submit():
        if 'user_id' not in session:
            flash('You need to log in first!')
            return redirect(url_for('view_shop', shop_id=shop_id))
        if shop in user.bookmarked_shops:
            user.bookmarked_shops.remove(shop)
            db.session.commit()
            flash('You have successfully remove the shop from your bookmarks!')
        return redirect(url_for('view_shop', shop_id=shop_id))

    return render_template('shop.html',
        logout_form=logout_form, add_bookmark_form=add_bookmark_form,
        delete_bookmark_form=delete_bookmark_form,
        welcome=welcome, shop=shop, products=products
    )


@app.route('/product_<int:product_id>', methods=['GET', 'POST'])
def view_product(product_id):
    welcome = 'Welcome!'
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        welcome += ' ID: {} Name: {}'.format(user.user_id, user.user_name)
    product = Product.query.get(product_id)
    logout_form = LogoutForm()
    if logout_form.submit_logout.data and logout_form.validate_on_submit():
        if 'user_id' in session:
            session.pop('user_id')
            flash('You have successfully signed out!')
        return redirect(url_for('index'))
    return render_template('product.html', logout_form=logout_form, welcome=welcome, product=product)
