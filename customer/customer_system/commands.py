# -*- coding: utf-8 -*-

import click

from customer_system import app, db
from customer_system.models import User


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
@click.option('--count', default=20, help='Quantity of instances, default is 20.')
def forge(count):
    """Generate fake instances."""
    import random
    from faker import Faker

    click.confirm('This operation will delete the old database, do you want to continue?', abort=True)
    db.drop_all()
    db.create_all()
    fake = Faker()
    click.echo('Working...')

    for i in range(count):
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

    db.session.commit()
    click.echo('Created {} fake instances.'.format(count))

@app.cli.command()
def viewdb():
    """Show the database content."""
    click.echo(db.session.execute('select * from users').fetchall())
