# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
import click

from shopSystem import app, db
from shopSystem.models import Shop, Product
import base64,random

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
