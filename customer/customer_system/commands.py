# -*- coding: utf-8 -*-

import click

from customer_system import app, db
from customer_system.models import *


@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
    if drop:
        click.confirm('This operation will delete the old database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized database.')


@app.cli.command()
@click.option('--count', default=10, help='Quantity of instances, default is 20.')
def forge(count):
    """Generate fake instances."""
    import random
    from faker import Faker

    click.confirm('This operation will delete the old database, do you want to continue?', abort=True)
    db.drop_all()
    db.create_all()
    fake = Faker()
    click.echo('Working...')

    shop_count = 0
    for i in range(1, count + 1):
        user = User(
            user_id = i,
            email = fake.safe_email(),
            user_password = fake.pystr(min_chars=1, max_chars=20),
            user_name = fake.name(),
            user_avatar = None,
            user_contact = fake.phone_number(),
            available_balance = fake.pyfloat(right_digits=2, min_value=0, max_value=10000),
            frozen_balance = fake.pyfloat(right_digits=2, min_value=0, max_value=10000),
            user_status = random.choice(['normal', 'blocked'])
        )
        db.session.add(user)

        for j in range(random.randint(0, 3)):
            shop_count += 1
            rate_number = random.randint(0, 100)
            rate_total = 0
            for k in range(rate_number):
                rate_total += random.randint(1, 5)
            shop = Shop(
                shop_id = shop_count,
                user_id = i,
                shop_name = fake.company(),
                shop_avatar = None,
                shop_info = fake.text(max_nb_chars=200),
                shop_delivery_fee = random.randint(0, 5),
                shop_rate_total = rate_total,
                shop_rate_number = rate_number,
                shop_balance = fake.pyfloat(right_digits=2, min_value=0, max_value=10000),
                shop_contact = fake.phone_number(),
                shop_location = random.choice(['Student Center', 'Shaw College', 'Deligentia College', 'Le Tian Building']),
                shop_location_detail = fake.sentence(nb_words=10, variable_nb_words=True),
                shop_license_number = fake.pystr_format(string_format='#' * 18),
                shop_status = random.choice(['open', 'closed', 'blocked', 'cancelled'])
            )
            db.session.add(shop)

            for l in range(random.randint(0, 10)):
                product = Product(
                    shop_id = shop_count,
                    product_name = fake.pystr(min_chars=1, max_chars=20),
                    product_avatar = None,
                    product_info = fake.text(max_nb_chars=200),
                    product_price = fake.pyfloat(right_digits=2, min_value=0, max_value=50),
                    total_sale = random.randint(0, 1000)
                )
                db.session.add(product)

    db.session.commit()
    click.echo('Created {} fake instances.'.format(count))


@app.cli.command()
def viewdb():
    """Show the database content."""
    click.echo(db.session.execute('SELECT * FROM administrators;').fetchall())
    click.echo(db.session.execute('SELECT * FROM users;').fetchall())
    click.echo(db.session.execute('SELECT * FROM shops;').fetchall())
    click.echo(db.session.execute('SELECT * FROM products;').fetchall())
    click.echo(db.session.execute('SELECT * FROM orders;').fetchall())
    click.echo(db.session.execute('SELECT * FROM purchased_products;').fetchall())
    click.echo(db.session.execute('SELECT * FROM applications;').fetchall())
    click.echo(db.session.execute('SELECT * FROM bookmarks;').fetchall())
