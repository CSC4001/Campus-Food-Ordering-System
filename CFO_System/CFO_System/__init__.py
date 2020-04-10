# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import os

import click

import base64,random

from flask import Flask, render_template


from CFO_System.settings import config
from CFO_System.blueprint.shop import shop_bp
from CFO_System.extensions import bootstrap, db, moment
from CFO_System.models import *

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG','development')
    app = Flask('CFO_System')
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)
    register_errors(app)
    register_commands(app)

    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    return app

def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)

def register_blueprints(app):
    app.register_blueprint(shop_bp, url_prefix='/my_shop')

def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')


    @app.cli.command()
    @click.option('--count', default=20, help='Quantity of messages, default is 20.')
    def forge(count):
        """Generate fake messages."""
        from faker import Faker

        db.drop_all()
        db.create_all()

        fake = Faker(locale='zh_CN')
        click.echo('Working...')
        status = ['正常营业','休息中','停业整顿','已关店']
        for i in range(count):
            #with open('static/favicon.ico','rb') as img:
            #   img=base64.b64encode(img.read())
            shop_message = Shop(
                user_id = str(fake.random_number(20)),
                shop_name = fake.company(),
                shop_info = fake.paragraph(3),
                shop_delivery_fee = fake.random_int(min=0,max=5),
                shop_rate = fake.random_int(),
                shop_rate_number = fake.random_int(),
                shop_balance = fake.random_number(),
                shop_contact = fake.phone_number(),
                shop_location = fake.street_address(),
                shop_location_detail = fake.address(),
                shop_license_number = str(fake.random_number(9)),
                shop_status = random.choice(status),
                # add avatar at the last step
                #shop_avatar = img
            )
            db.session.add(shop_message)

        shop_message = Shop(
            user_id = str(fake.random_number(20)),
            shop_name = "兰小花",
            shop_info = "卖牛肉面的",
            shop_delivery_fee = fake.random_int(min=0,max=5),
            shop_rate = fake.random_int(),
            shop_rate_number = fake.random_int(),
            shop_balance = fake.random_number(),
            shop_contact = fake.phone_number(),
            shop_location = "潘多拉",
            shop_location_detail = "学生活动中心一楼潘多拉美食广场",
            shop_license_number = str(fake.random_number(9)),
            shop_status = "正常营业",
            # add avatar at the last step
            #shop_avatar = img
        )
        db.session.add(shop_message)
        product_message = Product(
            product_name = "兰小花牛肉面",
            # product_avatar =
            product_info = "一碗牛肉面",
            product_price = 14,
            total_sale = 100
        )
        db.session.add(product_message)
        product_message.shop = shop_message
        db.session.commit()
        click.echo('Created %d fake messages.' % count)


